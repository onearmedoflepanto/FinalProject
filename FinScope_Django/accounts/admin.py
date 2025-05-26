from django.contrib import admin
from .models import User, FinancialProduct, ProductOption, SavedFinancialProduct
from .notifications import dispatch_rate_change_notifications # Import the notification function

class ProductOptionInline(admin.TabularInline): # Or admin.StackedInline
    model = ProductOption
    extra = 1 # Number of empty forms to display
    fields = ('save_trm', 'intr_rate_type', 'intr_rate_type_nm', 'intr_rate', 'intr_rate2')
    # readonly_fields = ('intr_rate_type_nm',) # Example if some fields are derived or not directly editable

class FinancialProductAdmin(admin.ModelAdmin):
    list_display = ('fin_prdt_nm', 'kor_co_nm', 'product_type', 'updated_at')
    list_display_links = ('fin_prdt_nm',) # Explicitly make fin_prdt_nm the link
    list_filter = ('product_type', 'kor_co_nm')
    search_fields = ('fin_prdt_nm', 'kor_co_nm', 'fin_prdt_cd')
    inlines = [ProductOptionInline]
    fieldsets = (
        (None, {
            'fields': (('fin_prdt_nm', 'kor_co_nm'), ('fin_co_no', 'fin_prdt_cd'), 'product_type')
        }),
        ('Details', {
            'classes': ('collapse',), # Collapsible section
            'fields': ('join_way', 'mtrt_int', 'spcl_cnd', 'join_deny', 'join_member', 'etc_note', 'max_limit')
        }),
        ('Disclosure Information', {
            'classes': ('collapse',),
            'fields': ('dcls_month', 'dcls_strt_day', 'dcls_end_day', 'fin_co_subm_day')
        }),
    )

class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('financial_product_name', 'save_trm', 'intr_rate_type', 'intr_rate', 'intr_rate2')
    list_filter = ('intr_rate_type', 'financial_product__kor_co_nm')
    search_fields = ('financial_product__fin_prdt_nm',)

    def financial_product_name(self, obj):
        return obj.financial_product.fin_prdt_nm
    financial_product_name.short_description = 'Financial Product'

    def save_model(self, request, obj: ProductOption, form, change):
        old_obj = None
        if obj.pk: # If this is a change to an existing object
            try:
                old_obj = ProductOption.objects.get(pk=obj.pk)
            except ProductOption.DoesNotExist:
                pass # Should not happen if obj.pk exists

        super().save_model(request, obj, form, change) # Save the object first

        if change and old_obj: # If it was an update
            new_rate = obj.intr_rate
            old_rate = old_obj.intr_rate
            
            # Check if intr_rate actually changed and both are not None
            if new_rate is not None and old_rate is not None and float(new_rate) != float(old_rate):
                self.message_user(request, f"Interest rate for {obj.financial_product.fin_prdt_nm} (Term: {obj.save_trm}m) changed from {old_rate}% to {new_rate}%. Dispatching notifications.")
                dispatch_rate_change_notifications(
                    financial_product=obj.financial_product,
                    changed_option_term=obj.save_trm,
                    old_rate=float(old_rate),
                    new_rate=float(new_rate)
                )
            elif new_rate is not None and old_rate is None: # Rate added
                 self.message_user(request, f"New interest rate {new_rate}% added for {obj.financial_product.fin_prdt_nm} (Term: {obj.save_trm}m).")
                 # Optionally, decide if adding a new rate where none existed should trigger notifications
                 # For now, only changes to existing rates trigger.
        elif not change and obj.intr_rate is not None: # If it's a new option being added with a rate
            self.message_user(request, f"New product option with rate {obj.intr_rate}% added for {obj.financial_product.fin_prdt_nm} (Term: {obj.save_trm}m).")


class SavedFinancialProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_display_name', 'product_type', 'notify_on_rate_change', 'saved_at')
    list_filter = ('product_type', 'notify_on_rate_change', 'user')
    search_fields = ('user__username', 'product_name', 'bank_name', 'fin_co_no', 'fin_prdt_cd')
    readonly_fields = ('saved_at',)
    fields = ('user', 'financial_product_ref', ('product_type', 'fin_co_no', 'fin_prdt_cd'), ('product_name', 'bank_name'), 'interest_rate_12m', 'notify_on_rate_change', 'saved_at')

    def product_display_name(self, obj):
        if obj.financial_product_ref:
            return obj.financial_product_ref.fin_prdt_nm
        return obj.product_name or "N/A"
    product_display_name.short_description = "Product Name"


admin.site.register(User) # Assuming UserAdmin is default or defined elsewhere
admin.site.register(FinancialProduct, FinancialProductAdmin)
admin.site.register(ProductOption, ProductOptionAdmin) # Register separately for its save_model to be effective
admin.site.register(SavedFinancialProduct, SavedFinancialProductAdmin)
