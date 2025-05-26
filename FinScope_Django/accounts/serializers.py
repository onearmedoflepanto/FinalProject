from rest_framework import serializers
from django.contrib.auth import get_user_model
from boards.models import Post, Comment
# from boards.serializers import PostSerializer, CommentSerializer # Commented out if PostSerializer is not used here directly for FinancialProduct related views
from .models import SavedFinancialProduct, FinancialProduct, ProductOption # Import new models

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


class NotificationSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedFinancialProduct
        fields = ('id', 'notify_on_rate_change', 'product_name', 'bank_name', 'fin_co_no', 'fin_prdt_cd', 'product_type') # Include identifiers
        read_only_fields = ('id', 'product_name', 'bank_name', 'fin_co_no', 'fin_prdt_cd', 'product_type') # Only notify_on_rate_change is writable

class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ['intr_rate_type', 'intr_rate_type_nm', 'save_trm', 'intr_rate', 'intr_rate2']

class FinancialProductSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True, read_only=True) # Nested options

    class Meta:
        model = FinancialProduct
        fields = [
            'id', # PK of the FinancialProduct model itself
            'fin_co_no',
            'fin_prdt_cd',
            'product_type',
            'kor_co_nm',
            'fin_prdt_nm',
            'join_way',
            'mtrt_int',
            'spcl_cnd',
            'join_deny',
            'join_member',
            'etc_note',
            'max_limit',
            'dcls_strt_day',
            'dcls_end_day',
            'fin_co_subm_day',
            'options' # Include the serialized options
        ]
        # Add read_only_fields if some fields should not be updatable via this serializer directly
        # read_only_fields = ['fin_co_no', 'fin_prdt_cd', 'product_type'] # Example


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
        # Assuming PostSerializer is correctly imported or defined elsewhere if needed by UserSerializer
        from boards.serializers import PostSerializer # Ensure it's available
        posts = Post.objects.filter(author=obj).order_by('-created_at')
        request = self.context.get('request')
        return PostSerializer(posts, many=True, context={'request': request}).data

    def get_authored_comments(self, obj):
        # Assuming CommentSerializer is correctly imported or defined elsewhere if needed by UserSerializer
        from boards.serializers import CommentSerializer # Ensure it's available
        comments = Comment.objects.filter(user=obj).order_by('-created_at')
        request = self.context.get('request')
        return CommentSerializer(comments, many=True, context={'request': request}).data
