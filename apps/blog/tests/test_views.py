from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.blog.models import Post, Comment


class PostAPITests(APITestCase):
    """Test case for Post API endpoints."""

    def setUp(self):
        # Create some initial posts
        self.post1 = Post.objects.create(title="Post 1", content="Content 1", author="Author 1")
        self.post2 = Post.objects.create(title="Post 2", content="Content 2", author="Author 2")
        
        # URLs
        self.list_create_url = reverse('post-list')
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post1.pk})

    def test_create_post(self):
        """Test creating a new post."""
        data = {'title': 'New Post', 'content': 'New Content', 'author': 'New Author'}
        response = self.client.post(self.list_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(Post.objects.get(title='New Post').author, 'New Author')

    def test_list_posts(self):
        """Test retrieving a list of posts."""
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Because we have pagination

    def test_retrieve_post(self):
        """Test retrieving a specific post."""
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Post 1')

    def test_update_post(self):
        """Test updating a post."""
        data = {'title': 'Updated Post', 'content': 'Updated Content', 'author': 'Updated Author'}
        response = self.client.put(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Post')
        self.assertEqual(self.post1.content, 'Updated Content')

    def test_delete_post(self):
        """Test deleting a post."""
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)


class CommentAPITests(APITestCase):
    """Test case for Comment API endpoints."""

    def setUp(self):
        # Create a post
        self.post = Post.objects.create(title="Test Post", content="Test Content", author="Test Author")
        
        # Create some comments
        self.comment1 = Comment.objects.create(content="Comment 1", post=self.post, author="Commenter 1")
        self.comment2 = Comment.objects.create(content="Comment 2", post=self.post, author="Commenter 2")
        
        # URLs
        self.list_create_url = reverse('comment-list-create', kwargs={'post_id': self.post.pk})
        self.detail_url = reverse('comment-detail', kwargs={'post_id': self.post.pk, 'pk': self.comment1.pk})

    def test_create_comment(self):
        """Test creating a new comment."""
        data = {'content': 'New Comment', 'author': 'New Commenter'}
        response = self.client.post(self.list_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)
        self.assertEqual(Comment.objects.get(content='New Comment').author, 'New Commenter')

    def test_list_comments(self):
        """Test retrieving a list of comments for a post."""
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # No pagination for comments

    def test_retrieve_comment(self):
        """Test retrieving a specific comment."""
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Comment 1')

    def test_delete_comment(self):
        """Test deleting a comment."""
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 1) 