from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import CommentForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy


def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Welcome to the Yee C W'
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def post_detail(request, pk):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(post_id=pk)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
        return HttpResponseRedirect(reverse('blog:comment-posted'))

    else:
        comment_form = CommentForm(initial={
            'author_id': request.user,
            'post': pk
        })

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, template_name, context)


def commented(request):
    return render(request, 'blog/comment_posted.html')


class PostCreateView(UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    group_required = u"Blog Authors"

    def get_success_url(self):
        return reverse_lazy('blog:post-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.groups.filter(name="Blog Authors").exists()

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


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    comment_form = CommentForm
    fields = ['content']


def about(request):
    return render(request, 'blog/about.html')
