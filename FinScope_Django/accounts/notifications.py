from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string # For more complex email templates later
from .models import FinancialProduct, SavedFinancialProduct, User

def dispatch_rate_change_notifications(financial_product: FinancialProduct, changed_option_term: str, old_rate: float, new_rate: float):
    """
    Sends email notifications to users subscribed to a financial product when its rate changes.

    Args:
        financial_product: The FinancialProduct instance that had a rate change.
        changed_option_term: The term of the rate that changed (e.g., "6", "12", "24").
        old_rate: The previous interest rate.
        new_rate: The new interest rate.
    """
    
    subscribed_saved_products = SavedFinancialProduct.objects.filter(
        financial_product_ref=financial_product,
        notify_on_rate_change=True
    ).select_related('user')

    if not subscribed_saved_products.exists():
        print(f"No users subscribed for notifications on product: {financial_product.fin_prdt_nm}")
        return 0 # No emails sent

    email_count = 0
    for saved_product_instance in subscribed_saved_products:
        user = saved_product_instance.user
        
        subject = f"[FinScope] 금리 변동 알림: {financial_product.fin_prdt_nm}"
        
        # Simple text email body for now. Can be replaced with HTML templates later.
        message_body = (
            f"안녕하세요 {user.nickname or user.username}님,\n\n"
            f"회원님께서 알림을 신청하신 금융상품 '{financial_product.fin_prdt_nm}' ({financial_product.kor_co_nm})의 금리가 변동되었습니다.\n\n"
            f"구분: {changed_option_term}개월 금리\n"
            f"이전 금리: {old_rate}%\n"
            f"현재 금리: {new_rate}%\n\n"
            f"자세한 내용은 FinScope 웹사이트에서 확인해주세요.\n\n"
            f"감사합니다.\nFinScope 팀"
        )
        
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        
        try:
            send_mail(
                subject,
                message_body,
                from_email,
                recipient_list,
                fail_silently=False,
            )
            print(f"Rate change notification email sent to {user.email} for product '{financial_product.fin_prdt_nm}'.")
            email_count += 1
        except Exception as e:
            print(f"Error sending rate change notification email to {user.email} for product '{financial_product.fin_prdt_nm}': {e}")
            # Consider logging this error more formally in a real application
            
    return email_count