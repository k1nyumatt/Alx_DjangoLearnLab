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