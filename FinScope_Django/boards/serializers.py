from rest_framework import serializers
from .models import Comment, Post # Import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    likes_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField() # Add this line

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'updated_at', 'views', 'likes', 'bookmarks']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_bookmarks_count(self, obj):
        return obj.bookmarks.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(id=request.user.id).exists()
        return False

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_comments(self, obj):
        # We need to import CommentSerializer here or ensure it's defined before PostSerializer
        # For simplicity, assuming CommentSerializer is defined above or imported correctly.
        comments = Comment.objects.filter(post=obj).order_by('created_at')
        serializer = CommentSerializer(comments, many=True, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True) # Added post title
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__' # This will include post_title if it's a property or annotation on model, or added above
        # Explicitly list fields to be sure:
        # fields = ['id', 'user', 'user_id', 'post', 'post_title', 'content', 'created_at', 'updated_at', 'is_following']
        read_only_fields = ['user', 'post', 'created_at']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user.followers.filter(id=request.user.id).exists()
        return False
