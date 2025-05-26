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

class SavedFinancialProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_financial_products')
    product_type = models.CharField(max_length=20)  # e.g., 'deposit', 'savings'
    fin_co_no = models.CharField(max_length=50)     # Financial company code from FSS
    fin_prdt_cd = models.CharField(max_length=50)   # Financial product code from FSS
    
    # Denormalized fields for easier display, populated when saving
    product_name = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    interest_rate_12m = models.FloatField(null=True, blank=True) # Store the 12-month rate at time of saving
    # You could add other rates like interest_rate_6m if needed

    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_type', 'fin_co_no', 'fin_prdt_cd')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} - {self.product_name} ({self.product_type})"
