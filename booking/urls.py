from django.urls import path
from .views import RoomBookingCreateView, PackageBookingCreateView

urlpatterns = [
    path('room-booking/', RoomBookingCreateView.as_view(), name='room-booking-create'),
    path('package-booking/', PackageBookingCreateView.as_view(), name='package-booking-create'),
]