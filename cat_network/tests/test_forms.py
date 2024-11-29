from django.test import TestCase
from django.contrib.auth import get_user_model
from cat_network.forms import CatUserCreationForm, PostSearchForm, CatSearchForm
from cat_network.models import CatUser, Post


class CatUserCreationFormTest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "Test",
            "age": 3,
        }

    def test_valid_form(self):
        form = CatUserCreationForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        invalid_data = self.user_data.copy()
        invalid_data["password2"] = "wrongpassword"
        form = CatUserCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_cleaned_data(self):
        form = CatUserCreationForm(data=self.user_data)
        form.is_valid()
        self.assertEqual(form.cleaned_data["username"], self.user_data["username"])
        self.assertEqual(form.cleaned_data["first_name"], self.user_data["first_name"])
        self.assertEqual(form.cleaned_data["age"], self.user_data["age"])


class PostSearchFormTest(TestCase):
    def setUp(self):
        user1 = CatUser.objects.create(username="catuser1", first_name="Cat", age=2)
        user2 = CatUser.objects.create(username="catuser2", first_name="Dog", age=3)

        Post.objects.create(
            title="First post", body="Content of first post", author=user1
        )
        Post.objects.create(
            title="Second post", body="Content of second post", author=user2
        )
        Post.objects.create(
            title="Another post", body="Content of another post", author=user1
        )

    def test_search_form_fields(self):
        form = PostSearchForm()
        self.assertIn("title", form.fields)

    def test_search_form_empty_data(self):
        form = PostSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_valid_data(self):
        form = PostSearchForm(data={"title": "First"})
        self.assertTrue(form.is_valid())

    def test_search_form_filter(self):
        form = PostSearchForm(data={"title": "post"})
        self.assertTrue(form.is_valid())
        filtered_posts = Post.objects.filter(
            title__icontains=form.cleaned_data["title"]
        )
        self.assertEqual(filtered_posts.count(), 3)
        self.assertIn("First post", [post.title for post in filtered_posts])
        self.assertIn("Second post", [post.title for post in filtered_posts])


class CatSearchFormTest(TestCase):
    def setUp(self):
        CatUser.objects.create(username="catuser1", first_name="Cat", age=2)
        CatUser.objects.create(username="catuser2", first_name="Dog", age=3)

    def test_search_form_fields(self):
        form = CatSearchForm()
        self.assertIn("username", form.fields)

    def test_search_form_empty_data(self):
        form = CatSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_valid_data(self):
        form = CatSearchForm(data={"username": "cat"})
        self.assertTrue(form.is_valid())

    def test_search_form_filter(self):
        form = CatSearchForm(data={"username": "cat"})
        self.assertTrue(form.is_valid())
        filtered_users = CatUser.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertEqual(filtered_users.count(), 2)
        self.assertIn("catuser1", [user.username for user in filtered_users])
