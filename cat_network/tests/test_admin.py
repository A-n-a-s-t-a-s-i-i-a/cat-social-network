from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from cat_network.models import Post, Comment, Like


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password",
        )
        self.client.force_login(self.admin_user)
        self.cat_user = get_user_model().objects.create_user(
            username="catuser",
            password="password",
            breed="Persian",
            age=5,
            bio="A cute cat.",
        )
        self.post = Post.objects.create(
            title="First Post", body="body of the first post", author=self.cat_user
        )
        self.comment = Comment.objects.create(
            text="This is a comment.", author=self.cat_user, post=self.post
        )
        self.like = Like.objects.create(user=self.cat_user, post=self.post)

    def test_cat_user_breed_listed(self):
        """
        Test that breed is listed in the CatUser admin page.
        """
        url = reverse("admin:cat_network_catuser_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.cat_user.breed)

    def test_cat_user_add_fields_listed(self):
        """
        Test that fields are listed as expected on the CatUser add page.
        """
        url = reverse("admin:cat_network_catuser_add")
        response = self.client.get(url)
        self.assertContains(response, "breed")
        self.assertContains(response, "age")
        self.assertContains(response, "profile_picture")

    def test_post_list_filter(self):
        """
        Test that post's author is used as a filter in the Post admin page.
        """
        url = reverse("admin:cat_network_post_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.post.title)

    def test_comment_list_filter(self):
        """
        Test that comment's author and post are used as filters in the Comment admin page.
        """
        url = reverse("admin:cat_network_comment_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.comment.text)

    def test_like_list_filter(self):
        """
        Test that like's user and post are used as filters in the Like admin page.
        """
        url = reverse("admin:cat_network_like_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.like.post.title)

