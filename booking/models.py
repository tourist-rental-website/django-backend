from django.db import models
from listings.models import Room, Package
from accounts.models import User
# Create your models here.

class RoomBooking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    traveler = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="room_bookings"
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    check_in = models.DateField()
    check_out = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.traveler.email} - {self.room}"
    
class PackageBooking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    traveler = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="package_bookings"
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    start_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.traveler.email} - {self.package.title}"
    



    