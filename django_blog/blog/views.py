from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'blog/profile.html', {'user': request.user})

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, PostForm
from .models import Post

# Keep your existing authentication views (register, user_login, user_logout, profile)
# ... (existing auth views here) ...

# Blog Post CRUD Views

class PostListView(ListView):
    """
    Display all blog posts to all users (authenticated or not).
    Posts are ordered by published_date (newest first).
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5  # Show 5 posts per page


class PostDetailView(DetailView):
    """
    Display a single blog post.
    Accessible to all users.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create new blog posts.
    Automatically sets the author to the logged-in user.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')
    
    def form_valid(self, form):
        """Set the post author to the current logged-in user"""
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow post authors to edit their own posts.
    Only the author can access this view.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the post"""
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow post authors to delete their own posts.
    Only the author can access this view.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        """Check if the current user is the author of the post"""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, PostForm, CommentForm
from .models import Post, Comment

# Keep your existing authentication views
# ... (register, user_login, user_logout, profile) ...

# Blog Post Views
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class PostDetailView(DetailView):
    """
    Display a single blog post with all its comments.
    Also includes a form for authenticated users to add comments.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add comment form to context
        context['comment_form'] = CommentForm()
        # Add all comments for this post
        context['comments'] = self.object.comments.all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Comment Views

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to add comments to blog posts.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        # Get the post object
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Set the comment's post and author
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect back to the post detail page
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow comment authors to edit their own comments.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the comment author"""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        # Redirect back to the post detail page
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        context['is_edit'] = True
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow comment authors to delete their own comments.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        """Check if the current user is the comment author"""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        # Redirect back to the post detail page
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

from django.db.models import Q
from taggit.models import Tag

# Search and Tag Views

def search_posts(request):
    """
    Search for posts based on title, content, or tags.
    Uses Q objects for complex queries.
    """
    query = request.GET.get('q', '')
    results = Post.objects.none()  # Empty queryset by default
    
    if query:
        # Search in title, content, and tags
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    context = {
        'query': query,
        'results': results,
        'results_count': results.count()
    }
    
    return render(request, 'blog/search_results.html', context)


def posts_by_tag(request, tag_name):
    """
    Display all posts associated with a specific tag.
    """
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags__name=tag_name)
    
    context = {
        'tag': tag,
        'posts': posts,
        'posts_count': posts.count()
    }
    
    return render(request, 'blog/posts_by_tag.html', context)


class TagListView(ListView):
    """
    Display all available tags with post counts.
    """
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
    
    def get_queryset(self):
        # Get all tags that are actually used
        return Tag.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add post count for each tag
        tags_with_counts = []
        for tag in context['tags']:
            count = Post.objects.filter(tags__name=tag.name).count()
            tags_with_counts.append({'tag': tag, 'count': count})
        context['tags_with_counts'] = tags_with_counts
        return context