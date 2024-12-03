from django.contrib.auth import get_user_model
from django.test import TestCase

from cat_network.models import Post, Comment, Like


class ModelTests(TestCase):
    def test_get_user_model_str(self):
        user = get_user_model().objects.create_user(
            username="CatLover123",
            password="password123",
            age=5,
            breed="Maine Coon",
            bio="I love climbing trees and chasing lasers!",
        )
        self.assertEqual(str(user), user.username)

    def test_post_str(self):
        user = get_user_model().objects.create_user(
            username="CatLover123",
            password="password123",
        )
        post = Post.objects.create(
            author=user,
            title="A Day in the Life of a Cat",
            body="Today, I climbed a tree and saw a bird!",
        )
        self.assertEqual(str(post), f"{post.title} - {post.author}")

    def test_comment_str(self):
        user = get_user_model().objects.create_user(
            username="CatLover123",
            password="password123",
        )
        post = Post.objects.create(
            author=user,
            title="A Day in the Life of a Cat",
            body="Today, I climbed a tree and saw a bird!",
        )
        comment = Comment.objects.create(
            author=user,
            post=post,
            text="This is so relatable!",
        )
        self.assertEqual(str(comment), f"{comment.post} - {comment.text}")

    def test_like_str(self):
        user = get_user_model().objects.create_user(
            username="CatLover123",
            password="password123",
        )
        post = Post.objects.create(
            author=user,
            title="A Day in the Life of a Cat",
            body="Today, I climbed a tree and saw a bird!",
        )
        like = Like.objects.create(user=user, post=post)
        self.assertEqual(str(like), f"{like.user} - {like.post} - Like")

    def test_create_get_user_model_with_followers(self):
        user1 = get_user_model().objects.create_user(
            username="CatFan",
            password="password123",
        )
        user2 = get_user_model().objects.create_user(
            username="LaserHunter",
            password="password123",
        )
        user1.followers.add(user2)
        self.assertIn(user2, user1.followers.all())
