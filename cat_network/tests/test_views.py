from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from cat_network.models import Post, Like, Comment, CatUser

POST_LIST_URL = reverse('cat_network:post-list')
POST_DETAIL_URL = reverse('cat_network:post-detail', kwargs={'pk': 1})
POST_CREATE_URL = reverse('cat_network:post-create')


class PublicPostTests(TestCase):
    def test_post_list_view_login_required(self):
        response = self.client.get(POST_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_login_required(self):
        response = self.client.get(POST_DETAIL_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivatePostTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.force_login(self.user)

    def test_retrieve_post_list(self):
        Post.objects.create(title="Test post 1", body="Test body", author=self.user)
        Post.objects.create(title="Test post 2", body="Test body 2", author=self.user)
        response = self.client.get(POST_LIST_URL)
        self.assertEqual(response.status_code, 200)
        posts = Post.objects.all()
        self.assertEqual(len(response.context["post_list"]), len(posts))

    def test_post_detail_view(self):
        post = Post.objects.create(title="Test post", body="Test body", author=self.user)
        response = self.client.get(reverse("cat_network:post-detail", kwargs={"pk": post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)

    def test_post_create_view(self):
        form_data = {
            "title": "Test post",
            "body": "Test body",
        }
        response = self.client.post(POST_CREATE_URL, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cat_network:post-list'))
        new_post = Post.objects.get(title="Test post")
        self.assertEqual(new_post.body, "Test body")


class PostLikeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.force_login(self.user)
        self.post = Post.objects.create(title="Test post", body="Test body", author=self.user)

    def test_toggle_like_post(self):
        response = self.client.post(reverse('cat_network:toggle-like'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 302)
        like = Like.objects.filter(user=self.user, post=self.post)
        self.assertEqual(like.count(), 1)

        response = self.client.post(reverse('cat_network:toggle-like'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 302)
        like = Like.objects.filter(user=self.user, post=self.post)
        self.assertEqual(like.count(), 0)


class CommentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.force_login(self.user)
        self.post = Post.objects.create(title="Test post", body="Test body", author=self.user)

    def test_comment_create_view(self):
        form_data = {
            "text": "Test comment",
        }
        response = self.client.post(reverse('cat_network:comment-create', kwargs={'pk': self.post.id}), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cat_network:comment-list', kwargs={'pk': self.post.id}))
        new_comment = Comment.objects.get(text="Test comment")
        self.assertEqual(new_comment.text, "Test comment")
        self.assertEqual(new_comment.author, self.user)
        self.assertEqual(new_comment.post, self.post)

    def test_comment_update_view(self):
        comment = Comment.objects.create(text="Original comment", author=self.user, post=self.post)
        form_data = {
            "text": "Updated comment",
        }
        response = self.client.post(reverse('cat_network:comment-update', kwargs={'pk': comment.id}), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cat_network:comment-list', kwargs={'pk': self.post.id}))
        updated_comment = Comment.objects.get(id=comment.id)
        self.assertEqual(updated_comment.text, "Updated comment")

    def test_comment_delete_view(self):
        comment = Comment.objects.create(text="Comment to delete", author=self.user, post=self.post)
        response = self.client.post(reverse('cat_network:comment-delete', kwargs={'pk': comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cat_network:comment-list', kwargs={'pk': self.post.id}))


class CatUserTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.force_login(self.user)

    def test_cat_user_list_view(self):
        CatUser.objects.create(username="catuser1", first_name="Cat", last_name="User")
        CatUser.objects.create(username="catuser2", first_name="Another", last_name="User")
        response = self.client.get(reverse('cat_network:cat-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "catuser1")
        self.assertContains(response, "catuser2")

    def test_cat_user_detail_view(self):
        cat_user = CatUser.objects.create(username="catuser", first_name="Cat", last_name="User")
        response = self.client.get(reverse('cat_network:cat-detail', kwargs={'pk': cat_user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, cat_user.username)

    def test_cat_user_create_view(self):
        form_data = {
            'username': 'newcatuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'age': 25,
        }

        response = self.client.post(reverse('cat_network:registration'), data=form_data)

        self.assertEqual(response.status_code, 302)

        new_user = CatUser.objects.get(username='newcatuser')
        self.assertEqual(new_user.username, 'newcatuser')

        self.assertRedirects(response, reverse('cat_network:cat-detail', kwargs={'pk': new_user.pk}))


class CatUserUpdateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.force_login(self.user)

    def test_cat_user_update_view(self):
        user = CatUser.objects.create(username="catuser", first_name="Cat", last_name="User")
        form_data = {
            "username": "updatedcatuser",
            "first_name": "Updated Cat",
            "bio": "Updated bio",
            "age": 6,
            "breed": "American Curl"
        }

        self.client.login(username="catuser", password="password")
        response = self.client.post(reverse('cat_network:cat-update', kwargs={'pk': user.id}), data=form_data)

        self.assertEqual(response.status_code, 302)
        updated_user = CatUser.objects.get(id=user.id)
        self.assertEqual(updated_user.username, "updatedcatuser")
        self.assertEqual(updated_user.first_name, "Updated Cat")
        self.assertEqual(updated_user.bio, "Updated bio")
        self.assertRedirects(response, reverse('cat_network:cat-detail', kwargs={'pk': updated_user.pk}))


class CatUserFollowersTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.force_login(self.user)
        self.cat = CatUser.objects.create(username="catuser", first_name="Cat", last_name="User")
        self.cat.followers.add(self.user)

    def test_cat_user_followers_view(self):
        response = self.client.get(reverse('cat_network:cat-followers', kwargs={'pk': self.cat.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)


class FollowCatUserTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.force_login(self.user)
        self.cat = CatUser.objects.create(username="catuser", first_name="Cat", last_name="User")

    def test_follow_catuser(self):
        response = self.client.post(reverse('cat_network:follow-catuser', kwargs={'pk': self.cat.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user in self.cat.followers.all())

    def test_unfollow_catuser(self):
        self.cat.followers.add(self.user)
        response = self.client.post(reverse('cat_network:follow-catuser', kwargs={'pk': self.cat.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user in self.cat.followers.all())

