import requests
import os # For path joining
from datetime import datetime # Import datetime for parsing
from django.utils import timezone # Import timezone for making datetimes aware
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as django_settings # Rename to avoid conflict
from django.db import transaction
from accounts.models import FinancialProduct, ProductOption
from accounts.notifications import dispatch_rate_change_notifications
from decouple import Config, RepositoryEnv # Import Config and RepositoryEnv

# Explicitly load .env from the Django project's base directory
# Assuming .env is in the same directory as manage.py
# BASE_DIR should be FinScope_Django directory
# settings.BASE_DIR from django.conf might not be fully initialized here, so construct path carefully
# Path to the .env file, assuming this command is in FinScope_Django/accounts/management/commands/
# So, ../../../.env relative to this file should be FinScope_Django/.env
# More robust: use settings.BASE_DIR if available and correctly points to FinScope_Django
# For now, let's assume .env is in the same dir as manage.py
# We'll use the BASE_DIR from the loaded django_settings
# This assumes that django_settings.BASE_DIR is correctly defined as the FinScope_Django project root.
# If not, this path needs to be adjusted.
# The .env file should be at the root of your Django project (FinScope_Django)
# config_loader = Config(RepositoryEnv(os.path.join(django_settings.BASE_DIR, '.env')))
# VITE_FSS_API_KEY_FROM_CMD = config_loader('VITE_FSS_API_KEY', default=None)
# This direct loading within the command is a fallback if settings isn't working as expected.
# The primary way should be through settings.py loading it.

FSS_BASE_URL = 'https://finlife.fss.or.kr/finlifeapi/'
PRODUCT_TYPES = {
    'deposit': 'depositProductsSearch.json',
    'savings': 'savingProductsSearch.json',
}
TOP_FIN_GRP_NO = '020000' # 은행 (Banks)

class Command(BaseCommand):
    help = 'Fetches financial product data (deposits and savings) from FSS, stores it, and triggers notifications on rate changes.'

    def fetch_fss_data_for_type(self, product_type_key, product_type_endpoint):
        """Fetches all pages for a given product type from FSS."""
        fss_api_key = getattr(django_settings, 'VITE_FSS_API_KEY', None)
        
        if not fss_api_key:
            self.stderr.write(self.style.ERROR(
                "Debug: django_settings.VITE_FSS_API_KEY is None or not found."
            ))
            # You can add more debug here, e.g., print(dir(django_settings)) to see all available settings
            # Or check if .env is even being found by settings.py:
            # print(f"Debug: settings.BASE_DIR is {django_settings.BASE_DIR}")
            # print(f"Debug: .env path checked by settings.py would be {os.path.join(django_settings.BASE_DIR, '.env')}")
            # print(f"Debug: Does that .env exist? {os.path.exists(os.path.join(django_settings.BASE_DIR, '.env'))}")
            raise CommandError(
                "FSS_API_KEY not found via django.conf.settings. "
                "Please ensure VITE_FSS_API_KEY is correctly set in your FinScope_Django/.env file (same dir as manage.py), "
                "and that settings.py loads it via `config('VITE_FSS_API_KEY', default=None)`."
            )
        else:
            self.stdout.write(self.style.SUCCESS("Successfully loaded FSS_API_KEY from Django settings."))

        all_products_base = []
        all_products_options = []
        page_no = 1
        max_pages_to_fetch = 10 # Safety break for development, FSS might have many pages. Adjust as needed.

        self.stdout.write(f"Fetching {product_type_key} products...")
        while True:
            if page_no > max_pages_to_fetch:
                self.stdout.write(self.style.WARNING(f"Reached max_pages_to_fetch ({max_pages_to_fetch}) for {product_type_key}. Stopping."))
                break
            
            api_url = f"{FSS_BASE_URL}{product_type_endpoint}"
            params = {
                'auth': fss_api_key, # Use the key obtained
                'topFinGrpNo': TOP_FIN_GRP_NO,
                'pageNo': page_no
            }
            try:
                response = requests.get(api_url, params=params, timeout=30) # Added timeout
                response.raise_for_status() # Raise an exception for HTTP errors
                data = response.json()
            except requests.exceptions.RequestException as e:
                self.stderr.write(self.style.ERROR(f"Error fetching page {page_no} for {product_type_key}: {e}"))
                break # Stop on error for this product type

            result = data.get('result', {})
            base_list = result.get('baseList', [])
            option_list = result.get('optionList', [])

            if not base_list: # No more products or empty page
                self.stdout.write(f"No more {product_type_key} products found on page {page_no}.")
                break
            
            all_products_base.extend(base_list)
            all_products_options.extend(option_list)
            
            self.stdout.write(f"Fetched page {page_no} for {product_type_key} ({len(base_list)} base products).")

            # Check if this was the last page (FSS API specific logic might be needed if not simply empty)
            # For now, we rely on base_list being empty. Some APIs provide total_count and max_page_no.
            # If FSS API has 'max_page_no' in result, use it:
            # if page_no >= result.get('max_page_no', page_no + 1):
            #    break
            
            page_no += 1
        
        return all_products_base, all_products_options

    @transaction.atomic # Ensure all database operations are in a single transaction
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting FSS product data fetch and update..."))

        for product_type_key, endpoint in PRODUCT_TYPES.items():
            base_list, option_list = self.fetch_fss_data_for_type(product_type_key, endpoint)

            if not base_list:
                self.stdout.write(self.style.WARNING(f"No base products fetched for {product_type_key}. Skipping."))
                continue

            self.stdout.write(f"Processing {len(base_list)} base products for {product_type_key}...")

            for base_info in base_list:
                fin_co_no = base_info.get('fin_co_no')
                fin_prdt_cd = base_info.get('fin_prdt_cd')

                if not fin_co_no or not fin_prdt_cd:
                    self.stderr.write(self.style.ERROR(f"Skipping product with missing fin_co_no or fin_prdt_cd: {base_info}"))
                    continue

                # Update or create FinancialProduct
                product_defaults = {
                    'dcls_month': base_info.get('dcls_month'),
                    'kor_co_nm': base_info.get('kor_co_nm'),
                    'fin_prdt_nm': base_info.get('fin_prdt_nm'),
                    'join_way': base_info.get('join_way'),
                    'mtrt_int': base_info.get('mtrt_int'),
                    'spcl_cnd': base_info.get('spcl_cnd'),
                    'join_deny': base_info.get('join_deny'),
                    'join_member': base_info.get('join_member'),
                    'etc_note': base_info.get('etc_note'),
                    'max_limit': base_info.get('max_limit'),
                    # 'dcls_strt_day': base_info.get('dcls_strt_day'), # Will be handled below
                    # 'dcls_end_day': base_info.get('dcls_end_day'),   # Will be handled below
                    # 'fin_co_subm_day': base_info.get('fin_co_subm_day'), # Will be handled below
                    'product_type': product_type_key
                }

                # Handle date/datetime conversions
                dcls_strt_day_str = base_info.get('dcls_strt_day')
                if dcls_strt_day_str:
                    try:
                        product_defaults['dcls_strt_day'] = datetime.strptime(dcls_strt_day_str, '%Y%m%d').date()
                    except ValueError:
                        self.stderr.write(self.style.WARNING(f"Invalid dcls_strt_day format: {dcls_strt_day_str} for {fin_prdt_cd}. Skipping field."))
                        product_defaults['dcls_strt_day'] = None
                else:
                    product_defaults['dcls_strt_day'] = None
                
                dcls_end_day_str = base_info.get('dcls_end_day')
                if dcls_end_day_str:
                    try:
                        product_defaults['dcls_end_day'] = datetime.strptime(dcls_end_day_str, '%Y%m%d').date()
                    except ValueError:
                        self.stderr.write(self.style.WARNING(f"Invalid dcls_end_day format: {dcls_end_day_str} for {fin_prdt_cd}. Skipping field."))
                        product_defaults['dcls_end_day'] = None
                else:
                    product_defaults['dcls_end_day'] = None

                fin_co_subm_day_str = base_info.get('fin_co_subm_day')
                if fin_co_subm_day_str:
                    try:
                        # FSS format seems to be YYYYMMDDHHMM
                        naive_dt = datetime.strptime(fin_co_subm_day_str, '%Y%m%d%H%M')
                        # Make it timezone-aware using Django's current timezone
                        product_defaults['fin_co_subm_day'] = timezone.make_aware(naive_dt, timezone.get_current_timezone())
                    except ValueError:
                        self.stderr.write(self.style.WARNING(f"Invalid fin_co_subm_day format: {fin_co_subm_day_str} for {fin_prdt_cd}. Skipping field."))
                        product_defaults['fin_co_subm_day'] = None
                else:
                    product_defaults['fin_co_subm_day'] = None
                
                financial_product, created_fp = FinancialProduct.objects.update_or_create(
                    fin_co_no=fin_co_no,
                    fin_prdt_cd=fin_prdt_cd,
                    product_type=product_type_key, # Ensure product_type is part of the unique key for lookup
                    defaults=product_defaults
                )
                if created_fp:
                    self.stdout.write(f"Created FinancialProduct: {financial_product.fin_prdt_nm}")
                else:
                    self.stdout.write(f"Updated FinancialProduct: {financial_product.fin_prdt_nm}")

                # Process options for this product
                product_options_from_api = [opt for opt in option_list if opt.get('fin_co_no') == fin_co_no and opt.get('fin_prdt_cd') == fin_prdt_cd]
                
                for opt_info in product_options_from_api:
                    save_trm = opt_info.get('save_trm')
                    intr_rate_type = opt_info.get('intr_rate_type', 'S') # Default to 'S' if not provided

                    option_defaults = {
                        'intr_rate_type_nm': opt_info.get('intr_rate_type_nm'),
                        'intr_rate': opt_info.get('intr_rate'),
                        'intr_rate2': opt_info.get('intr_rate2')
                    }
                    
                    # Try to get existing option
                    existing_option = None
                    try:
                        existing_option = ProductOption.objects.get(
                            financial_product=financial_product,
                            save_trm=save_trm,
                            intr_rate_type=intr_rate_type
                        )
                        old_rate = existing_option.intr_rate
                    except ProductOption.DoesNotExist:
                        old_rate = None # No old rate if it's a new option

                    # Update or create ProductOption
                    product_option, created_po = ProductOption.objects.update_or_create(
                        financial_product=financial_product,
                        save_trm=save_trm,
                        intr_rate_type=intr_rate_type,
                        defaults=option_defaults
                    )

                    new_rate = product_option.intr_rate

                    if not created_po and old_rate is not None and new_rate is not None and float(old_rate) != float(new_rate):
                        self.stdout.write(self.style.NOTICE(
                            f"Rate changed for {financial_product.fin_prdt_nm} (Term: {save_trm}m, Type: {intr_rate_type}): "
                            f"{old_rate}% -> {new_rate}%. Dispatching notifications..."
                        ))
                        # Dispatch notifications
                        dispatch_rate_change_notifications(
                            financial_product=financial_product,
                            changed_option_term=save_trm,
                            old_rate=float(old_rate),
                            new_rate=float(new_rate)
                        )
                    elif created_po:
                         self.stdout.write(f"Created ProductOption for {financial_product.fin_prdt_nm} (Term: {save_trm}m)")
        
        self.stdout.write(self.style.SUCCESS("FSS product data fetch and update complete."))