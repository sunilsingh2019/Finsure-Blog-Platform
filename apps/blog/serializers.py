from rest_framework import serializers
from .models import Post, Comment, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model"""
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'post']
        read_only_fields = ['id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model"""
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='categories'
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 
                  'categories', 'category_ids', 'likes', 'dislikes']
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes', 'dislikes']


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for listing posts"""
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'categories', 'likes', 'dislikes']
        read_only_fields = ['id', 'likes', 'dislikes']


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