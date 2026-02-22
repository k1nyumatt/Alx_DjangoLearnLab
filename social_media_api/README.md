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