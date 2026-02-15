# Django Blog - CRUD Features Documentation

## Overview
Complete CRUD (Create, Read, Update, Delete) functionality for blog posts with proper authentication and permissions.

## Features

### 1. List All Posts (Read)
- **URL**: `/`
- **View**: `PostListView`
- **Access**: Public (all users)
- **Features**:
  - Shows all posts ordered by newest first
  - Displays title, author, date, and excerpt
  - Pagination (5 posts per page)
  - "Read More" links to full posts

### 2. View Post Detail (Read)
- **URL**: `/post/<id>/`
- **View**: `PostDetailView`
- **Access**: Public (all users)
- **Features**:
  - Shows full post content
  - Displays author and publication date
  - Edit/Delete buttons (only for post author)
  - Back to list navigation

### 3. Create New Post (Create)
- **URL**: `/post/new/`
- **View**: `PostCreateView`
- **Access**: Authenticated users only
- **Features**:
  - Form with title and content fields
  - Author automatically set to logged-in user
  - Form validation
  - Success message on creation
  - Redirects to post list

### 4. Edit Post (Update)
- **URL**: `/post/<id>/update/`
- **View**: `PostUpdateView`
- **Access**: Post author only
- **Features**:
  - Pre-filled form with existing data
  - Can update title and content
  - Permission check (403 if not author)
  - Success message on update
  - Redirects to post detail

### 5. Delete Post (Delete)
- **URL**: `/post/<id>/delete/`
- **View**: `PostDeleteView`
- **Access**: Post author only
- **Features**:
  - Confirmation page before deletion
  - Shows post preview
  - Permission check (403 if not author)
  - Success message on deletion
  - Redirects to post list

## Permission System

### Access Levels

**Public Access (No Login Required):**
- View post list
- View individual posts

**Authenticated Users:**
- Create new posts
- View own profile
- Access all public features

**Post Authors Only:**
- Edit their own posts
- Delete their own posts

### Implementation

**LoginRequiredMixin:**
```python
class PostCreateView(LoginRequiredMixin, CreateView):
    # Requires user to be logged in
```

**UserPassesTestMixin:**
```python
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```

## Code Structure

### Models (`blog/models.py`)
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
```

### Forms (`blog/forms.py`)
```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```

### Views (`blog/views.py`)
- `PostListView` - Display all posts
- `PostDetailView` - Display single post
- `PostCreateView` - Create new post
- `PostUpdateView` - Edit existing post
- `PostDeleteView` - Delete post

### Templates
- `post_list.html` - List of all posts
- `post_detail.html` - Single post view
- `post_form.html` - Create/edit form
- `post_confirm_delete.html` - Delete confirmation

## Testing Guide

### Test Create Post
```bash
1. Login to your account
2. Click "New Post" in navigation
3. Enter title: "My First Post"
4. Enter content: "This is my first blog post!"
5. Click "Create Post"
6. Verify redirect to post list
7. Verify post appears in list
```

### Test Edit Post
```bash
1. Login as post author
2. Navigate to your post detail page
3. Click "Edit Post" button
4. Modify title or content
5. Click "Update Post"
6. Verify changes appear
7. Verify success message
```

### Test Delete Post
```bash
1. Login as post author
2. Navigate to your post detail page
3. Click "Delete Post" button
4. See confirmation page
5. Click "Yes, Delete"
6. Verify redirect to post list
7. Verify post no longer appears
```

### Test Permissions
```bash
# Test unauthorized edit
1. Create post with User A
2. Login as User B
3. Try to access /post/1/update/
4. Should see 403 Forbidden

# Test unauthorized delete
1. Create post with User A
2. Login as User B
3. Try to access /post/1/delete/
4. Should see 403 Forbidden

# Test login required
1. Logout
2. Try to access /post/new/
3. Should redirect to /login/?next=/post/new/
```

## Security Features

### CSRF Protection
All forms include `{% csrf_token %}` to prevent Cross-Site Request Forgery.

### Permission Checks
- Create: Must be logged in
- Update: Must be author
- Delete: Must be author

### Automatic Author Assignment
```python
def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
```

## User Experience

### Messages Framework
- Success messages on create/update/delete
- Error messages on form validation
- Color-coded alerts (green/red/blue)

### Navigation
- Intuitive URLs
- Breadcrumb navigation
- Back links on detail pages
- Cancel buttons on forms

### Responsive Design
- Mobile-friendly layouts
- Hover effects on cards
- Clean, modern styling

## Common Issues & Solutions

### Issue: "User object has no attribute 'posts'"
**Solution**: Ensure ForeignKey has `related_name='posts'`

### Issue: 403 Forbidden when editing own post
**Solution**: Check `test_func()` returns True for author

### Issue: Author field shows in form
**Solution**: Ensure PostForm only includes ['title', 'content']

### Issue: Posts not ordered correctly
**Solution**: Add `ordering = ['-published_date']` to ListView

## Future Enhancements
- Comments system
- Categories/tags
- Search functionality
- Rich text editor
- Image uploads
- Draft posts
- Post scheduling

## API Reference

### URL Names (for use in templates)
- `post-list` - List all posts
- `post-detail` - View single post
- `post-create` - Create new post
- `post-update` - Edit post
- `post-delete` - Delete post

### Template Context Variables
- `posts` - QuerySet of posts (ListView)
- `post` - Single post object (DetailView)
- `form` - Post form (CreateView/UpdateView)