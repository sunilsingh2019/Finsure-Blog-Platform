from django.test import TestCase
from apps.blog.models import Post, Comment


class PostModelTest(TestCase):
    """Test case for the Post model."""

    def setUp(self):
        Post.objects.create(
            title="Test Post",
            content="This is a test post content.",
            author="Test Author"
        )

    def test_post_creation(self):
        post = Post.objects.get(title="Test Post")
        self.assertEqual(post.content, "This is a test post content.")
        self.assertEqual(post.author, "Test Author")
        self.assertTrue(post.created_at)
        self.assertTrue(post.updated_at)

    def test_post_str_representation(self):
        post = Post.objects.get(title="Test Post")
        self.assertEqual(str(post), "Test Post")


class CommentModelTest(TestCase):
    """Test case for the Comment model."""

    def setUp(self):
        post = Post.objects.create(
            title="Test Post",
            content="This is a test post content.",
            author="Test Author"
        )
        Comment.objects.create(
            content="This is a test comment.",
            post=post,
            author="Comment Author"
        )

    def test_comment_creation(self):
        comment = Comment.objects.get(content="This is a test comment.")
        self.assertEqual(comment.author, "Comment Author")
        self.assertEqual(comment.post.title, "Test Post")
        self.assertTrue(comment.created_at)
        self.assertTrue(comment.updated_at)

    def test_comment_str_representation(self):
        comment = Comment.objects.get(content="This is a test comment.")
        self.assertEqual(str(comment), "Comment by Comment Author on Test Post") 