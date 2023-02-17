from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from reads_me.constants import APP_NAME
from reads_me.models import Post

pagination_count = 24


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, f'{APP_NAME}/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = f'{APP_NAME}/post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-timestamp']
    paginate_by = 5


class PostCategoryView(ListView):
    model = Post
    template_name = f'{APP_NAME}/post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-timestamp']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs.get('category')).order_by('-timestamp')


class PostTopicView(PostCategoryView):
    def get_queryset(self):
        return Post.objects.filter(wikipedia_id=self.kwargs.get('wikipedia_id')).order_by('-timestamp')


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        post = Post.objects.filter(slug=self.kwargs.get('slug')).order_by('-timestamp').first()
        # post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.object.title
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False