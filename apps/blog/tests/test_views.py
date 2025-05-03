from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.blog.models import Post, Comment, Category


class CategoryAPITests(APITestCase):
    """Test case for Category API endpoints."""

    def setUp(self):
        # Create some initial categories
        self.category1 = Category.objects.create(name="Category 1", description="Description 1")
        self.category2 = Category.objects.create(name="Category 2", description="Description 2")
        
        # URLs
        self.list_create_url = reverse('category-list')
        self.detail_url = reverse('category-detail', kwargs={'pk': self.category1.pk})

    def test_create_category(self):
        """Test creating a new category."""
        data = {'name': 'New Category', 'description': 'New Description'}
        response = self.client.post(self.list_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.get(name='New Category').description, 'New Description')

    def test_list_categories(self):
        """Test retrieving a list of categories."""
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We have 2 categories without pagination

    def test_retrieve_category(self):
        """Test retrieving a specific category."""
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Category 1')

    def test_update_category(self):
        """Test updating a category."""
        data = {'name': 'Updated Category', 'description': 'Updated Description'}
        response = self.client.put(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'Updated Category')
        self.assertEqual(self.category1.description, 'Updated Description')

    def test_delete_category(self):
        """Test deleting a category."""
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)


class PostAPITests(APITestCase):
    """Test case for Post API endpoints."""

    def setUp(self):
        # Create some initial posts (2 posts)
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
        self.assertEqual(len(response.data['results']), 2)  # We have 2 posts total

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
        
    def test_pagination(self):
        """Test pagination with multiple pages."""
        # Create 10 more posts (for a total of 12)
        for i in range(3, 13):
            Post.objects.create(
                title=f"Post {i}",
                content=f"Content {i}",
                author=f"Author {i}"
            )
        
        # Test first page
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # PAGE_SIZE is 5
        self.assertEqual(response.data['count'], 12)  # Total of 12 posts
        self.assertIsNotNone(response.data['next'])  # Should have a next page
        self.assertIsNone(response.data['previous'])  # No previous page
        
        # Test second page
        response = self.client.get(response.data['next'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # PAGE_SIZE is 5
        self.assertIsNotNone(response.data['next'])  # Should have a next page (3rd)
        self.assertIsNotNone(response.data['previous'])  # Should have a previous page
        
        # Test third page
        response = self.client.get(response.data['next'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 remaining posts
        self.assertIsNone(response.data['next'])  # No next page
        self.assertIsNotNone(response.data['previous'])  # Should have a previous page
        
        # Test invalid page
        response = self.client.get(f"{self.list_create_url}?page=999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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

    def test_update_comment(self):
        """Test updating a comment."""
        data = {'content': 'Updated Comment', 'author': 'Updated Commenter'}
        response = self.client.put(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.content, 'Updated Comment')
        self.assertEqual(self.comment1.author, 'Updated Commenter')

    def test_delete_comment(self):
        """Test deleting a comment."""
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 1)


class PermissionsTests(APITestCase):
    """Test case for checking permissions."""

    def setUp(self):
        # Create a post
        self.post = Post.objects.create(title="Test Post", content="Test Content", author="User A")
        
        # Create a comment
        self.comment = Comment.objects.create(content="Test Comment", post=self.post, author="User A")
        
        # URLs
        self.post_url = reverse('post-detail', kwargs={'pk': self.post.pk})
        self.comment_url = reverse('comment-detail', kwargs={'post_id': self.post.pk, 'pk': self.comment.pk})

    def test_different_user_can_update_post(self):
        """Test that a different user can update another user's post."""
        data = {'title': 'Updated by User B', 'content': 'Content updated by User B', 'author': 'User B'}
        response = self.client.put(self.post_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated by User B')
        self.assertEqual(self.post.author, 'User B')  # Author changed to User B

    def test_different_user_can_delete_post(self):
        """Test that a different user can delete another user's post."""
        response = self.client.delete(self.post_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_different_user_can_update_comment(self):
        """Test that a different user can update another user's comment."""
        data = {'content': 'Comment updated by User B', 'author': 'User B'}
        response = self.client.put(self.comment_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Comment updated by User B')
        self.assertEqual(self.comment.author, 'User B')  # Author changed to User B

    def test_different_user_can_delete_comment(self):
        """Test that a different user can delete another user's comment."""
        response = self.client.delete(self.comment_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0) 