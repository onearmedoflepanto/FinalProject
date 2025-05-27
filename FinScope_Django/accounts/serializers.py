from rest_framework import serializers
from django.contrib.auth import get_user_model
from boards.models import Post, Comment
from boards.serializers import PostSerializer, CommentSerializer
# from stocks.serializers import StockSerializer # Removed import
from .models import SavedFinancialProduct, BookmarkedVideo, SavedAiRecommendation # Import the new models

User = get_user_model() # Define User model

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # Use defined User
        fields = ("id", "nickname")

class SavedFinancialProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedFinancialProduct
        fields = ('id', 'product_type', 'fin_co_no', 'fin_prdt_cd', 'product_name', 'bank_name', 'interest_rate_12m', 'saved_at')
        read_only_fields = ('user', 'saved_at')

class BookmarkedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookmarkedVideo
        fields = ('id', 'video_id', 'title', 'thumbnail_url', 'channel_title', 'published_at', 'saved_at')
        read_only_fields = ('user', 'saved_at')

class SavedAiRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedAiRecommendation
        fields = ('id', 'recommendation_data', 'user_profile_at_recommendation', 'saved_at')
        read_only_fields = ('user', 'saved_at')


class UserSerializer(serializers.ModelSerializer):
    followings = UserSimpleSerializer(many=True, read_only=True)
    followers = UserSimpleSerializer(many=True, read_only=True)
    authored_posts = serializers.SerializerMethodField()
    authored_comments = serializers.SerializerMethodField()
    saved_financial_products = SavedFinancialProductSerializer(many=True, read_only=True)
    bookmarked_videos = BookmarkedVideoSerializer(many=True, read_only=True) 
    saved_ai_recommendations = SavedAiRecommendationSerializer(many=True, read_only=True)
    # favorite_stocks = StockSerializer(many=True, read_only=True) # Removed favorite stocks
    bookmarked_posts = PostSerializer(many=True, read_only=True) 


    class Meta:
        model = User # Use defined User
        fields = ("id", "username", "email", "nickname",
                  "age", "assets", "salary", "investment_tendency", 
                  "followings", "followers",
                  "authored_posts", "authored_comments",
                  "saved_financial_products", "bookmarked_videos",
                  "saved_ai_recommendations", # "favorite_stocks", # Removed favorite_stocks
                  "bookmarked_posts") 
        read_only_fields = ("username",)

    def get_authored_posts(self, obj):
        posts = Post.objects.filter(author=obj).order_by('-created_at')
        request = self.context.get('request')
        return PostSerializer(posts, many=True, context={'request': request}).data

    def get_authored_comments(self, obj):
        comments = Comment.objects.filter(user=obj).order_by('-created_at')
        request = self.context.get('request')
        return CommentSerializer(comments, many=True, context={'request': request}).data
