from django.urls import path

from cat_network.models import CatUser
from cat_network.views import index, PostListView, PostDetailView, PostCreateView, ToggleLikeView, CommentListView, \
    CommentCreateView, CatUserListView, CatUserCreateView

urlpatterns = [
    path('', index, name='index'),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path('toggle-like/', ToggleLikeView.as_view(), name='toggle-like'),
    path("posts/<int:pk>/comments/", CommentListView.as_view(), name="comment-list"),
    path("posts/<int:pk>/comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("cats/", CatUserListView.as_view(), name="cat-list"),
    path("registration/", CatUserCreateView.as_view(), name="registration"),
]


app_name = "cat_network"