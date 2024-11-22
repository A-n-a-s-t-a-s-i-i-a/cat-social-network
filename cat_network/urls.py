from django.urls import path

from cat_network.views import index, PostListView, PostDetailView, PostCreateView

urlpatterns = [
    path('', index, name='index'),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
]


app_name = "cat_network"