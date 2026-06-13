from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager): # Custom user manager to handle user creation with email instead of username
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser): # Custom user model extending AbstractUser to include a role field
# AbstractUser uses 'username' as the unique identifier by default, but we will override it to use 'email' instead
    objects = UserManager()  # Use the custom user manager    
    username = None  # Remove the username field
    email = models.EmailField(unique=True)  # Use email as the unique identifier for authentication
    ROLE_CHOICES = (
        ("traveler", "Traveler"),
        ("guide", "Guide"),
        ("hotel", "Hotel"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)  # Optional phone number field

    USERNAME_FIELD = 'email'  # Set email as the field used for authentication
    REQUIRED_FIELDS = []  # No additional required fields

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email'
            )
        ]
    
