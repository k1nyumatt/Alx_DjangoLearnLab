from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)  # optional text about yourself
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',               # references the same model (user follows user)
        symmetrical=False,    # if A follows B, B doesn't auto-follow A
        related_name='following',
        blank=True
    )