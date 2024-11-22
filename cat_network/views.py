from audioop import reverse

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from cat_network.models import Post, Comment, Like, CatUser


def index(request) -> HttpResponse:
    num_posts = Post.objects.count()
    num_comments = Comment.objects.count()
    num_likes = Like.objects.count()
    num_cats = CatUser.objects.count()
    context = {
        'num_posts': num_posts,
        'num_comments': num_comments,
        'num_likes': num_likes,
        'num_cats': num_cats,
    }
    return render(request, "cat_network/index.html", context=context)



class PostListView(ListView):
    model = Post
    template_name = "cat_network/post_list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "cat_network/post_detail.html"


class PostCreateView(CreateView):
    model = Post
    fields = "__all__"
    success_url = reverse_lazy("cat_network:post-list")
    template_name = "cat_network/post_create.html"
