# Django Permissions and Groups Setup

## Overview
This application implements a role-based access control system using Django's built-in permissions and groups functionality. Users are assigned to groups that determine what actions they can perform on Book objects.

## Custom Permissions

### Book Model Permissions
The following custom permissions have been added to the Book model in `relationship_app/models.py`:

- `can_view`: Allows users to view the list of books
- `can_create`: Allows users to create new books
- `can_edit`: Allows users to edit existing books
- `can_delete`: Allows users to delete books

These permissions are defined in the Book model's Meta class:
```python
class Meta:
    permissions = [
        ("can_view", "Can view book"),
        ("can_create", "Can create book"),
        ("can_edit", "Can edit book"),
        ("can_delete", "Can delete book"),
    ]
```

## Groups and Their Permissions

### 1. Viewers Group
**Permissions:**
- `can_view` - Can view the book list

**Access Level:**
- Can only view books
- Cannot create, edit, or delete books

### 2. Editors Group
**Permissions:**
- `can_view` - Can view the book list
- `can_create` - Can add new books
- `can_edit` - Can modify existing books

**Access Level:**
- Can view, create, and edit books
- Cannot delete books

### 3. Admins Group
**Permissions:**
- `can_view` - Can view the book list
- `can_create` - Can add new books
- `can_edit` - Can modify existing books
- `can_delete` - Can remove books

**Access Level:**
- Full access to all book operations

## How Permissions Are Enforced

### In Views (views.py)
Permissions are enforced using the `@permission_required` decorator:
```python
@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    # View implementation
```

The `raise_exception=True` parameter ensures that users without the required permission receive a 403 Forbidden error instead of being redirected to the login page.

### In Templates
Templates check permissions before displaying action buttons:
```html
{% if perms.relationship_app.can_create %}
    <a href="{% url 'book_create' %}">Add New Book</a>
{% endif %}
```

This ensures that users only see options for actions they're permitted to perform.

## Setup Instructions

### 1. Create Groups
In Django Admin:
1. Navigate to "Groups"
2. Create three groups: Viewers, Editors, Admins
3. Assign the appropriate permissions to each group as listed above

### 2. Assign Users to Groups
In Django Admin:
1. Go to "Users"
2. Select a user
3. Scroll to the "Groups" section
4. Move the desired group from "Available groups" to "Chosen groups"
5. Save

### 3. Testing Permissions
- Log in as users from different groups
- Attempt to access different views
- Verify that permissions are enforced correctly

## URLs for Testing

- Book List: `/relationship/books/`
- Create Book: `/relationship/books/create/`
- Edit Book: `/relationship/books/<id>/edit/`
- Delete Book: `/relationship/books/<id>/delete/`

## Security Notes

- All views are protected with `@permission_required` decorators
- Users without proper permissions receive 403 Forbidden errors
- Templates conditionally display UI elements based on user permissions
- The `raise_exception=True` parameter prevents unauthorized access attempts