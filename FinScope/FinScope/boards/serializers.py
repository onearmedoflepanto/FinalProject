from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'stock', 'created_at']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user.followers.filter(id=request.user.id).exists()
        return False