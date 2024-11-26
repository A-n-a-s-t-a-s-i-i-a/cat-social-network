from django.urls import path

from cat_network.models import CatUser
from cat_network.views import index, PostListView, PostDetailView, PostCreateView, ToggleLikeView, CommentListView, \
    CommentCreateView, CatUserListView, CatUserCreateView, CommentUpdateView, CommentDeleteView, CatUserDetailView, \
    follow_catuser, CatUserFollowersView

urlpatterns = [
    path('', index, name='index'),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path('toggle-like/', ToggleLikeView.as_view(), name='toggle-like'),
    path("posts/<int:pk>/comments/", CommentListView.as_view(), name="comment-list"),
    path("posts/<int:pk>/comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    path("cats/", CatUserListView.as_view(), name="cat-list"),
    path('catuser/<int:pk>/follow/', follow_catuser, name='follow-catuser'),
    path("cats/<int:pk>/", CatUserDetailView.as_view(), name="cat-detail"),
    path("cats/<int:pk>/followers/", CatUserFollowersView.as_view(), name="cat-followers"),
    path("registration/", CatUserCreateView.as_view(), name="registration"),
]


app_name = "cat_network"