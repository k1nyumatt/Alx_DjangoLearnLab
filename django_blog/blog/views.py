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