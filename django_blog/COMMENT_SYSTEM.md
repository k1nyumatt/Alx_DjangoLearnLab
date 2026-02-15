# Django Blog - Comment System Documentation

## Overview
A complete comment system that allows authenticated users to engage in discussions on blog posts. Users can create, read, update, and delete their own comments.

## Features

### 1. View Comments (Read)
- **Access**: Public (all users)
- **Location**: Post detail page
- **Features**:
  - Shows all comments for a post
  - Displays comment count
  - Shows author and timestamp
  - Indicates edited comments
  - Ordered chronologically (oldest first)

### 2. Add Comments (Create)
- **Access**: Authenticated users only
- **Location**: Post detail page (inline form)
- **Features**:
  - Quick comment form on post page
  - Auto-sets post and author
  - Validates non-empty content
  - Success message on creation
  - Stays on same post page

### 3. Edit Comments (Update)
- **Access**: Comment author only
- **Location**: Separate edit page
- **Features**:
  - Pre-filled form with existing comment
  - Shows post context
  - Updates timestamp
  - Shows "(edited)" indicator
  - Permission check (403 if not author)

### 4. Delete Comments (Delete)
- **Access**: Comment author only
- **Location**: Confirmation page
- **Features**:
  - Shows comment preview
  - Requires confirmation
  - Permission check (403 if not author)
  - Success message on deletion

## Database Model

### Comment Model
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Relationships
- **Many-to-One with Post**: Each comment belongs to one post; a post can have many comments
- **Many-to-One with User**: Each comment has one author; a user can write many comments
- **Cascade Delete**: If post or user is deleted, their comments are deleted

## Permission System

### Access Levels

**Public (No Login Required):**
- View all comments on posts

**Authenticated Users:**
- Create new comments
- View their own comments
- Access all public features

**Comment Authors Only:**
- Edit their own comments
- Delete their own comments

### Implementation

**Login Required:**
```python
class CommentCreateView(LoginRequiredMixin, CreateView):
    # User must be logged in to comment
```

**Author-Only Access:**
```python
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
```

## URL Structure
```
POST /post/<post_id>/comments/new/     - Create comment
GET  /comment/<comment_id>/update/     - Edit form
POST /comment/<comment_id>/update/     - Submit edit
GET  /comment/<comment_id>/delete/     - Delete confirmation
POST /comment/<comment_id>/delete/     - Confirm delete
```

## User Workflows

### Adding a Comment
1. User views post detail page
2. Scrolls to comment section
3. Types comment in inline form
4. Clicks "Post Comment"
5. Comment appears immediately in list
6. Success message displayed

### Editing a Comment
1. User sees their comment with Edit button
2. Clicks "Edit"
3. Taken to edit form page (shows post context)
4. Modifies comment text
5. Clicks "Update Comment"
6. Redirected back to post
7. Comment shows "(edited)" label

### Deleting a Comment
1. User clicks "Delete" on their comment
2. Taken to confirmation page
3. Sees preview of comment to be deleted
4. Clicks "Yes, Delete Comment"
5. Redirected back to post
6. Comment is removed from list

## Template Integration

### Post Detail Template
- Displays comment count
- Shows comment form (if authenticated)
- Lists all comments
- Edit/Delete buttons (for own comments)
- Login prompt (if not authenticated)

### Comment Form Template
- Used for both create and edit
- Shows post context
- Single textarea for content
- Cancel button returns to post

### Delete Confirmation Template
- Shows comment preview
- Warning message
- Confirmation required
- Cancel button returns to post

## Form Validation

### Content Validation
```python
def clean_content(self):
    content = self.cleaned_data.get('content')
    if not content or not content.strip():
        raise forms.ValidationError('Comment cannot be empty.')
    return content
```

### Rules
- Comment cannot be empty
- Whitespace-only comments rejected
- Maximum length: unlimited (TextField)

## Testing Guide

### Test Adding Comment
```bash
1. Login to your account
2. Navigate to any post
3. Scroll to comments section
4. Type: "This is a great post!"
5. Click "Post Comment"
6. Verify comment appears at bottom of list
7. Verify your username is shown
8. Verify Edit/Delete buttons appear
```

### Test Editing Comment
```bash
1. Click "Edit" on your comment
2. Change text to: "This is an amazing post!"
3. Click "Update Comment"
4. Verify updated text appears
5. Verify "(edited)" label shows
6. Verify success message
```

### Test Deleting Comment
```bash
1. Click "Delete" on your comment
2. See confirmation page with comment preview
3. Click "Yes, Delete Comment"
4. Verify redirect to post page
5. Verify comment no longer in list
6. Verify success message
```

### Test Permissions
```bash
# Test unauthorized edit
1. User A creates comment (ID: 1)
2. Login as User B
3. Navigate to /comment/1/update/
4. Should see 403 Forbidden error

# Test unauthorized delete
1. User A creates comment (ID: 1)
2. Login as User B
3. Navigate to /comment/1/delete/
4. Should see 403 Forbidden error

# Test login required
1. Logout completely
2. Try to post comment
3. Comment form should not appear
4. Should see login prompt instead
```

### Test Validation
```bash
1. Try to submit empty comment
2. Should see error: "Comment cannot be empty"
3. Try comment with only spaces
4. Should see same error
5. Verify form does not submit
```

## Security Features

### CSRF Protection
All forms include `{% csrf_token %}` to prevent Cross-Site Request Forgery.

### Permission Checks
- Create: Must be logged in
- Update: Must be comment author
- Delete: Must be comment author

### Automatic Field Setting
```python
def form_valid(self, form):
    form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
    form.instance.author = self.request.user
    return super().form_valid(form)
```

### SQL Injection Prevention
- Django ORM handles all queries
- User input automatically escaped
- No raw SQL queries used

## Display Features

### Comment Metadata
- Author username
- Creation timestamp
- Last update timestamp
- "(edited)" indicator if modified

### Visual Design
- Clean card-based layout
- Hover effects
- Color-coded action buttons
- Responsive design

### User Experience
- Inline comment form (no page reload needed for viewing)
- Breadcrumb navigation
- Success/error messages
- Cancel buttons on all forms

## Common Issues & Solutions

### Issue: Comments not appearing
**Solution**: Check that comment is saved with correct post FK

### Issue: Edit/Delete buttons for all comments
**Solution**: Verify template checks `{% if user == comment.author %}`

### Issue: 403 error when editing own comment
**Solution**: Check test_func() returns True for author

### Issue: "(edited)" always showing
**Solution**: Check template: `{% if comment.created_at != comment.updated_at %}`

## Future Enhancements
- Comment replies (threaded comments)
- Comment likes/votes
- Comment moderation
- Markdown support
- Mention notifications (@username)
- Comment reactions (emoji)
- Comment sorting options
- Spam protection/CAPTCHA
- Comment flagging

## API Reference

### Model Methods
```python
# Get all comments for a post
post.comments.all()

# Get all comments by a user
user.comments.all()

# Count comments on a post
post.comments.count()
```

### URL Names
- `comment-create` - Create new comment
- `comment-update` - Edit comment
- `comment-delete` - Delete comment

### Template Variables
- `comments` - QuerySet of comments for a post
- `comment_form` - CommentForm instance
- `is_edit` - Boolean indicating edit mode