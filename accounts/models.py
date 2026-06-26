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
    profile_image = models.ImageField(blank=True, null=True)
    is_verified = models.BooleanField(default = False)
    USERNAME_FIELD = 'email'  # Set email as the field used for authentication
    REQUIRED_FIELDS = []  # No additional required fields

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email'
            )
        ]
    
class TravelerProfile(models.Model):
    user = models.OneToOneField( # One-to-one relationship with User model, just like foregin key but only one guide profile per user 
        User,                    # whereas foreign key allows multiple guide profiles for a single user
        on_delete=models.CASCADE,
        related_name="traveler_profile"
    )
    
