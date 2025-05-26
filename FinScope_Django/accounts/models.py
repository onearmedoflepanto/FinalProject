from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    assets = models.IntegerField(blank=True, null=True) # 자산
    salary = models.IntegerField(blank=True, null=True) # 연봉
    # 저축 성향 ('알뜰형', '균형형', '도전형')
    savings_tendency = models.CharField(max_length=50, blank=True, null=True) 
    
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    # Add any other fields you need for your user model
    # For example, if you want to store profile picture, etc.
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username

# Model to store detailed financial product information
class FinancialProduct(models.Model):
    fin_co_no = models.CharField(max_length=50)                     # 금융회사 코드
    fin_prdt_cd = models.CharField(max_length=50)                   # 금융상품 코드
    product_type = models.CharField(max_length=20)                  # 'deposit' or 'savings'
    
    dcls_month = models.CharField(max_length=6, null=True, blank=True) # 공시월
    kor_co_nm = models.CharField(max_length=100, null=True, blank=True) # 금융회사명
    fin_prdt_nm = models.CharField(max_length=255, null=True, blank=True) # 금융상품명
    join_way = models.TextField(null=True, blank=True)              # 가입 방법
    mtrt_int = models.TextField(null=True, blank=True)              # 만기 후 이자율
    spcl_cnd = models.TextField(null=True, blank=True)              # 우대 조건
    join_deny = models.CharField(max_length=50, null=True, blank=True) # 가입제한 (1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField(null=True, blank=True)           # 가입 대상
    etc_note = models.TextField(null=True, blank=True)              # 기타 유의사항
    max_limit = models.BigIntegerField(null=True, blank=True)       # 최고 한도
    dcls_strt_day = models.DateField(null=True, blank=True)         # 공시 시작일
    dcls_end_day = models.DateField(null=True, blank=True)          # 공시 종료일
    fin_co_subm_day = models.DateTimeField(null=True, blank=True)   # 금융회사 제출일

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('fin_co_no', 'fin_prdt_cd', 'product_type')
        verbose_name = "금융 상품"
        verbose_name_plural = "금융 상품들"

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm} ({self.product_type})"

# Model to store interest rate options for each financial product
class ProductOption(models.Model):
    financial_product = models.ForeignKey(FinancialProduct, related_name='options', on_delete=models.CASCADE)
    intr_rate_type = models.CharField(max_length=1, null=True, blank=True) # 저축 금리 유형 (S:단리, M:복리)
    intr_rate_type_nm = models.CharField(max_length=10, null=True, blank=True) # 저축 금리 유형명
    save_trm = models.CharField(max_length=3, null=True, blank=True)        # 저축 기간 (개월)
    intr_rate = models.FloatField(null=True, blank=True)                    # 저축 금리
    intr_rate2 = models.FloatField(null=True, blank=True)                   # 최고 우대금리

    class Meta:
        unique_together = ('financial_product', 'save_trm', 'intr_rate_type') # Ensure unique options per product term/type
        verbose_name = "상품 옵션 (금리)"
        verbose_name_plural = "상품 옵션 (금리들)"

    def __str__(self):
        return f"{self.financial_product.fin_prdt_nm} - {self.save_trm}개월: {self.intr_rate}%"


class SavedFinancialProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_financial_products')
    # Link to the new FinancialProduct model instead of storing codes directly
    # This assumes that a FinancialProduct entry will exist before it can be saved.
    # If products can be saved before their full details are in FinancialProduct,
    # then keep fin_co_no, fin_prdt_cd, product_type and add a nullable ForeignKey.
    # For simplicity now, let's assume FinancialProduct exists.
    financial_product_ref = models.ForeignKey(FinancialProduct, on_delete=models.CASCADE, null=True, blank=True, related_name='savers')
    
    # Keep these for now for compatibility or if financial_product_ref is not immediately available
    # Or, these could be removed if financial_product_ref is always set.
    product_type = models.CharField(max_length=20)  # e.g., 'deposit', 'savings'
    fin_co_no = models.CharField(max_length=50)     # Financial company code from FSS
    fin_prdt_cd = models.CharField(max_length=50)   # Financial product code from FSS
    
    # Denormalized fields for easier display, populated when saving
    product_name = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    interest_rate_12m = models.FloatField(null=True, blank=True) # Store the 12-month rate at time of saving
    
    notify_on_rate_change = models.BooleanField(default=False) # New field for notifications

    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # If using financial_product_ref as the primary link:
        # unique_together = ('user', 'financial_product_ref')
        # If keeping the old structure for identification:
        unique_together = ('user', 'product_type', 'fin_co_no', 'fin_prdt_cd')
        ordering = ['-saved_at']

    def __str__(self):
        if self.financial_product_ref:
            return f"{self.user.username} - {self.financial_product_ref.fin_prdt_nm} ({self.financial_product_ref.product_type})"
        return f"{self.user.username} - {self.product_name} ({self.product_type})"
