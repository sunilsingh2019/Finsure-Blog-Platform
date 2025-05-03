from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import (
    PostSerializer, 
    PostListSerializer,
    CommentSerializer,
    CommentListSerializer,
    CommentDetailSerializer
)

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for the Post model"""
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentCreateListView(generics.ListCreateAPIView):
    """View for creating and listing comments for a specific post"""
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentListSerializer
        return CommentSerializer
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        # Check if post exists
        get_object_or_404(Post, pk=post_id)
        
        data = request.data.copy()
        data['post'] = post_id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentDetailView(generics.RetrieveDestroyAPIView):
    """View for retrieving and deleting a specific comment"""
    serializer_class = CommentDetailSerializer
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)
    
    def get_object(self):
        queryset = self.get_queryset()
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(queryset, pk=comment_id)
        return comment
