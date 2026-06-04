from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): # Custom user model extending AbstractUser to include a role field

    ROLE_CHOICES = (
        ("traveler", "Traveler"),
        ("guide", "Guide"),
        ("hotel", "Hotel"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    