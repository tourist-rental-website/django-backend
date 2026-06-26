from django.db import models
from accounts.models import User


class GuideProfile(models.Model):
    user = models.OneToOneField( # One-to-one relationship with User model, just like foregin key but only one guide profile per user 
        User,                    # whereas foreign key allows multiple guide profiles for a single user
        on_delete=models.CASCADE,
        related_name="guide_profile"
    )

    bio = models.TextField(blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    languages = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Guide: {self.user.email}"

    class Meta:
        indexes = [
            models.Index(fields=["location"]),
        ]

class HotelProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="hotel_profile"
    )

    hotel_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    contact_number = models.CharField(max_length=20,blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hotel_name
    
    class Meta:
        indexes = [
            models.Index(fields=["location"]),
        ]

class Room(models.Model):
    hotel = models.ForeignKey(
        HotelProfile,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    ROOM_TYPE_CHOICES = (
        ("deluxe", "Deluxe"),
        ("standard", "Standard"),
        ("suite", "Suite"),
    )

    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_type} at {self.hotel.hotel_name}"
    
    class Meta:
        indexes = [
            models.Index(fields=["room_type"]),
            models.Index(fields=["is_available"]),
        ]

class RoomImage(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="room_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image of {self.room.room_type} room at {self.room.hotel.hotel_name}"

class Package(models.Model):
    guide = models.ForeignKey(
        GuideProfile,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    location = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.guide.user.email}"

    class Meta:
        indexes = [
            models.Index(fields=["price"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['guide', 'title'],
                name='unique_package_per_guide'
            )
        ]
        