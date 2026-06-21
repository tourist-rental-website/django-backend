from django.urls import path
from .views import (
    GuideProfileCreateView,
    GuideProfileListView,
    GuideProfileDetailView,
    HotelProfileCreateView,
    HotelProfileListView,
    HotelProfileDetailView,
    PackageListView,
    PackageDetailView,
    RoomCreateView,
    RoomListView,
    RoomDetailView,
    PackageCreateView,
)

urlpatterns = [
    #path("guides/create/", GuideProfileCreateView.as_view(), name="guide-create"),
    path("guides/", GuideProfileListView.as_view(), name="guide-list"),
    path("guides/<int:pk>/", GuideProfileDetailView.as_view(), name="guide-detail"),
    path("hotels/create/", HotelProfileCreateView.as_view(), name="hotel-create"),
    path("hotels/", HotelProfileListView.as_view(), name="hotel-list"),
    path("hotels/<int:pk>/", HotelProfileDetailView.as_view(), name="hotel-detail"),
    path("rooms/create/", RoomCreateView.as_view(), name="room-create"),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDetailView.as_view(), name="room-detail"),
    path("packages/create/", PackageCreateView.as_view(), name="package-create"),
    path("packages/", PackageListView.as_view(), name="package-list"),
    path("packages/<int:pk>/", PackageDetailView.as_view(), name="package-detail"),
]
