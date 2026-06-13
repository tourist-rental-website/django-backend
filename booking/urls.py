from django.urls import path
from .views import CancelPackageBookingView, CancelRoomBookingView, MyBookingsView
from .views import MyPackageBookingsView, RoomBookingCreateView, PackageBookingCreateView

urlpatterns = [
    path('room-booking/', RoomBookingCreateView.as_view(), name='room-booking-create'),
    path('package-booking/', PackageBookingCreateView.as_view(), name='package-booking-create'),
    path('my-room-bookings/', MyBookingsView.as_view(), name='my-room-bookings'),
    path('my-package-bookings/', MyPackageBookingsView.as_view(), name='my-package-bookings'),
    path("room-bookings/<int:pk>/cancel/", CancelRoomBookingView.as_view(), name="cancel-room-booking"),
    path("package-bookings/<int:pk>/cancel/", CancelPackageBookingView.as_view(), name="cancel-package-booking"),
]