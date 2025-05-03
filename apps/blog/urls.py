from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentCreateListView, CommentDetailView, CategoryViewSet

# Create a router for viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)

# URL patterns for the blog app
urlpatterns = [
    # Comment URLs
    path('posts/<int:post_id>/comments/', CommentCreateListView.as_view(), name='comment-list-create'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]

# Add router URLs to urlpatterns
urlpatterns += router.urls 