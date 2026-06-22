from django.urls import path
from .views import GuideProfileUpdateView, GuideProfileListView, HotelProfileUpadateView, HotelProfileListView, PackageListView, RoomCreateView, RoomListView, PackageCreateView

urlpatterns = [
    path("guides/update/", GuideProfileUpdateView.as_view(), name="guide-update"),
    path("guides/", GuideProfileListView.as_view(), name="guide-list"),
    path("hotels/update/", HotelProfileUpadateView.as_view(), name="hotel-update"),
    path("hotels/", HotelProfileListView.as_view(), name="hotel-list"),
    path("rooms/create/", RoomCreateView.as_view(), name="room-create"),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("packages/create/", PackageCreateView.as_view(), name="package-create"),
    path("packages/", PackageListView.as_view(), name="package-list"),
]
