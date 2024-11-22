from audioop import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
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
    queryset = Post.objects.prefetch_related('like_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_liked_posts = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        context['user_liked_posts'] = set(user_liked_posts)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "cat_network/post_detail.html"


class PostCreateView(CreateView):
    model = Post
    fields = ("title", "body", "image")
    success_url = reverse_lazy("cat_network:post-list")
    template_name = "cat_network/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ToggleLikeView(View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()

        referer_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(f"{referer_url}#post-{post.id}")

