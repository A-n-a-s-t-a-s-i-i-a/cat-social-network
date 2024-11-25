from audioop import reverse

from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cat_network.forms import CatUserCreationForm, PostSearchForm, CatSearchForm
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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_liked_posts = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            context['user_liked_posts'] = set(user_liked_posts)
        else:
            context['user_liked_posts'] = set()
        title = self.request.GET.get('title', "")
        context['search_form'] = PostSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        queryset = Post.objects.prefetch_related('like_set')
        form = PostSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data['title'])
        return queryset


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "cat_network/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_liked_posts = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        context['user_liked_posts'] = set(user_liked_posts)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ("title", "body", "image")
    success_url = reverse_lazy("cat_network:post-list")
    template_name = "cat_network/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()

        referer_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(f"{referer_url}#post-{post.id}")


class CommentListView(ListView):
    model = Comment
    template_name = "cat_network/comment_list.html"
    context_object_name = 'comments'

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return Comment.objects.filter(post_id=post_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs.get('pk'))  # Передаем объект поста
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ("text",)
    template_name = "cat_network/comment_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cat_network:comment-list",   kwargs={"pk": self.kwargs["pk"]})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ("text",)
    template_name = "cat_network/comment_create.html"

    def get_success_url(self):
        return reverse_lazy("cat_network:comment-list",   kwargs={"pk": self.kwargs["pk"]})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "cat_network/comment_delete.html"

    def get_success_url(self):
        return reverse_lazy("cat_network:comment-list", kwargs={"pk": self.kwargs["pk"]})


class CatUserListView(ListView):
    model = CatUser
    template_name = "cat_network/cat_list.html"
    context_object_name = 'cat_users'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get('username', "")
        context['search_form'] = CatSearchForm(
            initial={"username": username}
        )
        context["catuser"] = self.request.user
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        form = CatSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data['username'])
        return queryset




class CatUserCreateView(CreateView):
    model = CatUser
    form_class = CatUserCreationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("cat_network:index")

    def form_valid(self, form):
        user = form.save()
        user.profile_picture = self.request.FILES.get('profile_picture')
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


class CatUserDetailView(DetailView):
    model = CatUser
    template_name = "cat_network/cat_detail.html"


@login_required
def follow_catuser(request, pk):
    cat = get_object_or_404(CatUser, pk=pk)
    print(f"ID cat: {pk}")
    catuser = request.user
    print(f"ID catuser: {catuser.id}")
    if catuser in cat.followers.all():
        cat.followers.remove(catuser)
    else:
        cat.followers.add(catuser)
    return redirect("cat_network:cat-list")
