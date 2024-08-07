from rest_framework import serializers
from .models import CustomUser, Post

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio']

class PostSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at']
