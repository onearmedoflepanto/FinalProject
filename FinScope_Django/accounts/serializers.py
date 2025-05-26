from rest_framework import serializers
from django.contrib.auth import get_user_model
from boards.models import Post, Comment
from boards.serializers import PostSerializer, CommentSerializer
from .models import SavedFinancialProduct # Import the new model

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


class UserSerializer(serializers.ModelSerializer):
    followings = UserSimpleSerializer(many=True, read_only=True)
    followers = UserSimpleSerializer(many=True, read_only=True)
    authored_posts = serializers.SerializerMethodField()
    authored_comments = serializers.SerializerMethodField()
    saved_financial_products = SavedFinancialProductSerializer(many=True, read_only=True)


    class Meta:
        model = User # Use defined User
        fields = ("id", "username", "email", "nickname", 
                  "followings", "followers",
                  "authored_posts", "authored_comments",
                  "saved_financial_products") # Added saved products
        read_only_fields = ("username",)

    def get_authored_posts(self, obj):
        posts = Post.objects.filter(author=obj).order_by('-created_at')
        request = self.context.get('request')
        return PostSerializer(posts, many=True, context={'request': request}).data

    def get_authored_comments(self, obj):
        comments = Comment.objects.filter(user=obj).order_by('-created_at')
        request = self.context.get('request')
        return CommentSerializer(comments, many=True, context={'request': request}).data
