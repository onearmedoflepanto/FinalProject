from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User, FinancialProduct, SavedFinancialProduct, ProductOption # Ensure all are imported

class Command(BaseCommand):
    help = 'Sends a test rate change notification email for a specific product to subscribed users.'

    def add_arguments(self, parser):
        parser.add_argument('product_id', type=int, help='The ID of the FinancialProduct to test notifications for.')
        parser.add_argument(
            '--new_rate',
            type=float,
            default=5.0, # A default new rate for the test
            help='The new interest rate to simulate for the notification.'
        )

    def handle(self, *args, **options):
        product_id = options['product_id']
        new_rate = options['new_rate']

        try:
            product = FinancialProduct.objects.get(pk=product_id)
        except FinancialProduct.DoesNotExist:
            raise CommandError(f'FinancialProduct with ID "{product_id}" does not exist.')

        # Find users who have this product saved and are subscribed to notifications
        # We need to iterate through SavedFinancialProduct instances
        subscribed_saved_products = SavedFinancialProduct.objects.filter(
            financial_product_ref=product, 
            notify_on_rate_change=True
        ).select_related('user')

        if not subscribed_saved_products.exists():
            self.stdout.write(self.style.WARNING(f'No users are subscribed to notifications for product: {product.fin_prdt_nm}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {subscribed_saved_products.count()} subscribed user(s) for {product.fin_prdt_nm}.'))

        for saved_product_instance in subscribed_saved_products:
            user = saved_product_instance.user
            subject = f'금리 변동 알림: {product.fin_prdt_nm}'
            message_body = (
                f"안녕하세요 {user.nickname or user.username}님,\n\n"
                f"회원님께서 알림을 신청하신 금융상품 '{product.fin_prdt_nm}' ({product.kor_co_nm})의 금리가 변동되었습니다.\n"
                f"새로운 (테스트) 12개월 금리: {new_rate}%\n\n"
                f"자세한 내용은 웹사이트에서 확인해주세요.\n\n"
                f"감사합니다.\nFinScope 팀"
            )
            from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@finscope.com'
            
            try:
                send_mail(
                    subject,
                    message_body,
                    from_email,
                    [user.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f'Test notification email sent to {user.email} for product ID {product.id}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error sending email to {user.email}: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Finished sending test notifications.'))