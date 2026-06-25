from django.urls import path
from .views import (
    GuideProfileUpdateView,
    GuideProfileListView,
    GuideProfileDetailView,
    HotelProfileUpadateView,
    HotelProfileListView,
    HotelProfileDetailView,
    PackageListView,
    PackageDetailView,
    RoomListCreateView,
    RoomDetailView,
    PackageCreateView,
    RoomImageUploadView
)
urlpatterns = [
    path("guides/update/", GuideProfileUpdateView.as_view(), name="guide-update"),
    path("guides/", GuideProfileListView.as_view(), name="guide-list"),
    path("guides/<int:pk>/", GuideProfileDetailView.as_view(), name="guide-detail"),
    path("hotels/update/", HotelProfileUpadateView.as_view(), name="hotel-update"),
    path("hotels/", HotelProfileListView.as_view(), name="hotel-list"),
    path("hotels/<int:pk>/", HotelProfileDetailView.as_view(), name="hotel-detail"),
    path(
        "rooms/",
        RoomListCreateView.as_view(),
        name="room-list-create"
    ),
    path("rooms/<int:pk>/", RoomDetailView.as_view(), name="room-detail"),

    path(
        "rooms/<int:room_id>/images/",
        RoomImageUploadView.as_view(),
        name="room-image-upload"
    ),
    path("packages/create/", PackageCreateView.as_view(), name="package-create"),
    path("packages/", PackageListView.as_view(), name="package-list"),
    path("packages/<int:pk>/", PackageDetailView.as_view(), name="package-detail"),
]
