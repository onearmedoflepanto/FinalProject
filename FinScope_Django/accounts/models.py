from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    assets = models.IntegerField(blank=True, null=True) # 자산
    salary = models.IntegerField(blank=True, null=True) # 연봉
    # 투자 성향 ('공격형', '중립형', '안정형')
    INVESTMENT_TENDENCY_CHOICES = [
        ('공격형', '공격형'),
        ('중립형', '중립형'),
        ('안정형', '안정형'),
    ]
    investment_tendency = models.CharField(
        max_length=50,
        choices=INVESTMENT_TENDENCY_CHOICES,
        blank=True,
        null=True
    )
    
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

class BookmarkedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_videos')
    video_id = models.CharField(max_length=255) # YouTube video ID
    title = models.CharField(max_length=512)
    thumbnail_url = models.URLField(max_length=512, blank=True, null=True)
    channel_title = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.CharField(max_length=100, blank=True, null=True) # Store as string from YouTube API (e.g., "2023-10-26")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video_id') # User can bookmark a video only once
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class SavedAiRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_ai_recommendations')
    # Storing the raw JSON response from Gemini, or a structured version of it
    # TextField is simpler if the structure is just a list of {"name": ..., "type": ...}
    # JSONField is better if you plan to query parts of the recommendation, but requires PostgreSQL or newer SQLite
    recommendation_data = models.TextField() # Stores the JSON string of recommendations
    user_profile_at_recommendation = models.JSONField(null=True, blank=True) # Snapshot of user profile used for this recommendation
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} - AI Recommendation saved at {self.saved_at.strftime('%Y-%m-%d %H:%M')}"
