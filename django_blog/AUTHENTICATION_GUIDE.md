# Django Blog Authentication System Documentation

## Overview
This authentication system provides complete user management functionality including registration, login, logout, and profile management.

## Features
- User Registration with email
- Secure Login/Logout
- Profile Management
- Password Security (PBKDF2 hashing)
- CSRF Protection
- User Feedback via Messages

## System Components

### 1. Forms (`blog/forms.py`)
- **CustomUserCreationForm**: Extended Django's UserCreationForm to include email field
- Validates username, email, and password
- Ensures password confirmation matches

### 2. Views (`blog/views.py`)

#### `register(request)`
- Handles user registration
- Auto-logs in new users
- Redirects to profile page

#### `user_login(request)`
- Authenticates users
- Handles login errors
- Redirects to profile page

#### `user_logout(request)`
- Logs out current user
- Redirects to login page

#### `profile(request)`
- Displays user information
- Allows email updates
- Requires authentication (@login_required)

### 3. Templates
- **base.html**: Main template with navigation
- **register.html**: Registration form
- **login.html**: Login form
- **profile.html**: User profile and editing

### 4. URL Configuration
```
/register/ - User registration
/login/ - User login
/logout/ - User logout
/profile/ - User profile (protected)
```

## Security Features

### CSRF Protection
All forms include `{% csrf_token %}` to prevent Cross-Site Request Forgery attacks.

### Password Security
- Django's built-in password hashing (PBKDF2)
- Password validation rules enforced
- Secure password storage

### Authentication Requirements
- Profile page requires login
- Unauthorized access redirects to login
- Session management handled by Django

## User Workflows

### Registration Flow
1. User visits /register/
2. Fills out username, email, password
3. Form validates input
4. User account created
5. Auto-login occurs
6. Redirect to profile

### Login Flow
1. User visits /login/
2. Enters username and password
3. System authenticates credentials
4. Success: Redirect to profile
5. Failure: Show error message

### Profile Management Flow
1. User must be logged in
2. Views current information
3. Can update email
4. Changes saved to database
5. Success message displayed

## Testing Instructions

### Test Registration
```bash
1. Navigate to http://127.0.0.1:8000/register/
2. Enter: username, email, password (twice)
3. Click "Register"
4. Verify auto-login and redirect to profile
```

### Test Login
```bash
1. Logout if logged in
2. Navigate to http://127.0.0.1:8000/login/
3. Enter credentials
4. Click "Login"
5. Verify redirect to profile
```

### Test Logout
```bash
1. While logged in, click "Logout" in navigation
2. Verify redirect to login page
3. Verify logged out state
```

### Test Profile Update
```bash
1. Login to your account
2. Navigate to profile page
3. Change email address
4. Click "Update Profile"
5. Verify success message
6. Verify email changed
```

### Test Security
```bash
1. Logout completely
2. Try to access http://127.0.0.1:8000/profile/
3. Should redirect to /login/?next=/profile/
4. This confirms @login_required works
```

## Troubleshooting

### Issue: "CSRF verification failed"
**Solution**: Ensure `{% csrf_token %}` is in all forms

### Issue: Can't login after registration
**Solution**: Check that user.save() is called in registration view

### Issue: Profile page not protected
**Solution**: Verify @login_required decorator on profile view

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic` and check STATIC_URL

## Future Enhancements
- Password reset functionality
- Email verification
- Social authentication (Google, GitHub)
- Two-factor authentication
- Profile pictures
- User bio/description fields

## Settings Configuration

Required settings in `settings.py`:
```python
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'
```

## Dependencies
- Django (built-in auth system)
- No additional packages required for basic auth