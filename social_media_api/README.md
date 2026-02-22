# Social Media API

A RESTful API built with Django and Django REST Framework for social media functionality, starting with user authentication.

---

## Setup & Installation

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd social_media_api
```

2. **Install dependencies**
```bash
   pip install django djangorestframework pillow
```

3. **Run migrations**
```bash
   python manage.py makemigrations
   python manage.py migrate
```

4. **Start the development server**
```bash
   python manage.py runserver
```

---

## User Model

The custom user model extends Django's `AbstractUser` with the following additional fields:

- `bio` — A short text description about the user
- `profile_picture` — An optional profile image
- `followers` — A many-to-many relationship to other users (asymmetric, like Instagram)

---

## Authentication

This API uses **token-based authentication**. After registering or logging in, you receive a token that must be included in the header of authenticated requests:
```
Authorization: Token <your_token_here>
```

---

## API Endpoints

### Register
- **URL:** `POST /api/accounts/register/`
- **Body:**
```json
  {
    "username": "john",
    "email": "john@example.com",
    "password": "yourpassword"
  }
```
- **Response:** Returns a token on success.

---

### Login
- **URL:** `POST /api/accounts/login/`
- **Body:**
```json
  {
    "username": "john",
    "password": "yourpassword"
  }
```
- **Response:** Returns the user's token.

---

### Profile
- **URL:** `GET /api/accounts/profile/`
- **Auth required:** Yes (`Authorization: Token <token>`)
- **Response:** Returns the authenticated user's profile data.

## Overview

This is a Social Media API built with Django and Django REST Framework. It allows users to register, log in, create posts, and comment on posts. Authentication is handled via tokens — you register or log in and receive a token that you use for all protected actions.

---

## How to Run

1. Install dependencies: `pip install django djangorestframework pillow`
2. Run migrations: `python manage.py migrate`
3. Start the server: `python manage.py runserver`

---

## How Authentication Works

Register or log in to receive a token. Include it in every request that requires authentication:
```
Authorization: Token <your_token_here>
```

---

## Endpoints

| Method | URL | Description | Auth |
|--------|-----|-------------|------|
| POST | `/api/accounts/register/` | Create a new account | No |
| POST | `/api/accounts/login/` | Log in and get token | No |
| GET | `/api/accounts/profile/` | View your profile | Yes |
| GET | `/api/posts/` | List all posts | No |
| POST | `/api/posts/` | Create a post | Yes |
| GET | `/api/posts/<id>/` | View a single post | No |
| PUT | `/api/posts/<id>/` | Edit your post | Yes |
| DELETE | `/api/posts/<id>/` | Delete your post | Yes |
| GET | `/api/comments/` | List all comments | No |
| POST | `/api/comments/` | Add a comment | Yes |
| PUT | `/api/comments/<id>/` | Edit your comment | Yes |
| DELETE | `/api/comments/<id>/` | Delete your comment | Yes |

Posts can be searched using `?search=keyword` in the URL. Results are paginated, 10 per page.

## Social Media API

A RESTful API built with Django and Django REST Framework that supports user authentication, posting, commenting, following users, and a personal feed.

---

## Setup
```bash
pip install django djangorestframework pillow
python manage.py migrate
python manage.py runserver
```

---

## Authentication

Register or log in to receive a token. Send it with every protected request:
```
Authorization: Token <your_token_here>
```

---

## Endpoints

### Accounts

| Method | URL | Description | Auth Required |
|--------|-----|-------------|---------------|
| POST | `/api/accounts/register/` | Create a new account | No |
| POST | `/api/accounts/login/` | Log in and get token | No |
| GET | `/api/accounts/profile/` | View your profile | Yes |
| POST | `/api/accounts/follow/<id>/` | Follow a user | Yes |
| POST | `/api/accounts/unfollow/<id>/` | Unfollow a user | Yes |

### Posts & Comments

| Method | URL | Description | Auth Required |
|--------|-----|-------------|---------------|
| GET | `/api/posts/` | List all posts | No |
| POST | `/api/posts/` | Create a post | Yes |
| GET | `/api/posts/<id>/` | View a single post | No |
| PUT | `/api/posts/<id>/` | Edit your post | Yes |
| DELETE | `/api/posts/<id>/` | Delete your post | Yes |
| GET | `/api/posts/feed/` | View feed from followed users | Yes |
| GET | `/api/comments/` | List all comments | No |
| POST | `/api/comments/` | Add a comment | Yes |
| PUT | `/api/comments/<id>/` | Edit your comment | Yes |
| DELETE | `/api/comments/<id>/` | Delete your comment | Yes |

---

## Notes

- Posts can be searched using `?search=keyword` in the URL
- Results are paginated, 10 per page — use `?page=2` to navigate
- Only the author of a post or comment can edit or delete it
- The feed only shows posts from users you follow, ordered by newest first

## Likes & Notifications

### Like a Post
- **URL:** `POST /api/posts/<id>/like/`
- **Auth required:** Yes
- **Success Response:** `200 OK`
```json
  { "message": "Post liked" }
```
- **Already liked Response:** `400 Bad Request`
```json
  { "message": "You already liked this post" }
```

### Unlike a Post
- **URL:** `POST /api/posts/<id>/unlike/`
- **Auth required:** Yes
- **Success Response:** `200 OK`
```json
  { "message": "Post unliked" }
```
- **Not liked Response:** `400 Bad Request`
```json
  { "message": "You have not liked this post" }
```

### View Notifications
- **URL:** `GET /api/notifications/`
- **Auth required:** Yes
- **Success Response:** `200 OK`
```json
  [
    {
      "id": 1,
      "actor": "john",
      "verb": "liked your post",
      "is_read": false,
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
```
- **Note:** All notifications are marked as read after this endpoint is called.

---

## Testing

### User Registration
- **Action:** POST to `/api/accounts/register/` with username, email, and password
- **Expected:** Returns a token
- **Result:** Pass

### User Login
- **Action:** POST to `/api/accounts/login/` with username and password
- **Expected:** Returns the user token
- **Result:** Pass

### Follow a User
- **Action:** POST to `/api/accounts/follow/2/` with a valid token in the header
- **Expected:** Returns a success message confirming the follow
- **Result:** Pass

### Unfollow a User
- **Action:** POST to `/api/accounts/unfollow/2/` with a valid token in the header
- **Expected:** Returns a success message confirming the unfollow
- **Result:** Pass

### Create a Post
- **Action:** POST to `/api/posts/` with title and content, token in header
- **Expected:** Returns the created post object
- **Result:** Pass

### View Feed
- **Action:** GET to `/api/posts/feed/` with token in header
- **Expected:** Returns posts from followed users ordered by newest first
- **Result:** Pass

### Like a Post
- **Action:** POST to `/api/posts/1/like/` with token in header
- **Expected:** Returns like confirmation and creates a notification for the post author
- **Result:** Pass

### Like a Post Twice
- **Action:** POST to `/api/posts/1/like/` again with the same token
- **Expected:** Returns 400 error — already liked
- **Result:** Pass

### Unlike a Post
- **Action:** POST to `/api/posts/1/unlike/` with token in header
- **Expected:** Returns unlike confirmation
- **Result:** Pass

### View Notifications
- **Action:** GET to `/api/notifications/` with token in header
- **Expected:** Returns list of notifications, then marks them all as read
- **Result:** Pass

### Permission Enforcement
- **Action:** Try to edit or delete another user's post
- **Expected:** Returns 403 Forbidden
- **Result:** Pass

## Deployment

### Configuration Files
- `Procfile` — tells Heroku to use gunicorn as the web server
- `runtime.txt` — specifies the Python version
- `requirements.txt` — lists all project dependencies

### Environment Variables
The following environment variables must be set in production:
- `SECRET_KEY` — Django secret key
- `DATABASE_URL` — database connection URL
- `DEBUG` — set to False in production

### Deployment Steps
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables
3. Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic`
5. Start the server: `gunicorn social_media_api.wsgi`

### Security Settings
- DEBUG is set to False in production
- HTTPS is enforced via SECURE_SSL_REDIRECT
- XSS protection is enabled
- Clickjacking protection is enabled via X_FRAME_OPTIONS

### Maintenance
- Monitor logs regularly for errors
- Keep dependencies updated via pip
- Back up the database regularly

## Deployment Documentation

### Tools Used
- **Gunicorn** — production web server
- **Whitenoise** — serves static files
- **dj-database-url** — manages database configuration
- **Heroku** — cloud hosting platform

---

### Configuration Files

**Procfile**
```
web: gunicorn social_media_api.wsgi --log-file -
```

**runtime.txt**
```
python-3.11.0
```

**Key Production Settings in settings.py**
```
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

### Environment Variables

Set these on your hosting platform before deploying:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | Database connection URL |
| `DEBUG` | Set to False in production |

---

### Deployment Steps

1. Clone the repository
```bash
   git clone <your-repo-url>
   cd social_media_api
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Set environment variables
```bash
   heroku config:set SECRET_KEY='your-secret-key' --app your-app-name
   heroku config:set DEBUG=False --app your-app-name
```

4. Push to Heroku
```bash
   heroku git:remote -a your-app-name
   git push heroku master:main
```

5. Run migrations
```bash
   heroku run python manage.py migrate --app your-app-name
```

6. Collect static files
```bash
   heroku run python manage.py collectstatic --app your-app-name
```

---

### Live URL
```
https://social-media-api-matt.herokuapp.com/
```

---

### Maintenance Plan
- Monitor application logs regularly: `heroku logs --tail --app your-app-name`
- Keep all dependencies up to date by running `pip install -r requirements.txt` after any updates
- Back up the database before any major changes
- Rotate the SECRET_KEY periodically and update the environment variable on Heroku