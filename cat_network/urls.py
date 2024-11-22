from django.urls import path

from cat_network.views import index, PostListView, PostDetailView, PostCreateView, ToggleLikeView

urlpatterns = [
    path('', index, name='index'),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path('toggle-like/', ToggleLikeView.as_view(), name='toggle-like'),
]


app_name = "cat_network"