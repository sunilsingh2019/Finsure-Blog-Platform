from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model"""
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'post']
        read_only_fields = ['id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model"""
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for listing posts"""
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author']
        read_only_fields = ['id']


class CommentListSerializer(serializers.ModelSerializer):
    """Serializer for listing comments"""
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    """Serializer for comment details"""
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'created_at'] 