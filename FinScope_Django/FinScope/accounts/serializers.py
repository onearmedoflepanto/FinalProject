from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "nickname")

class UserSerializer(serializers.ModelSerializer):
    followings = UserSimpleSerializer(many=True, read_only=True)
    followers = UserSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "nickname", "followings", "followers")
        read_only_fields = ("username",)