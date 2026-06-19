from django.urls import path
from .views import GuideProfileCreateView, GuideProfileListView, HotelProfileCreateView, HotelProfileListView, PackageListView, RoomCreateView, RoomListView, PackageCreateView

urlpatterns = [
    #path("guides/create/", GuideProfileCreateView.as_view(), name="guide-create"),
    path("guides/", GuideProfileListView.as_view(), name="guide-list"),
    path("hotels/create/", HotelProfileCreateView.as_view(), name="hotel-create"),
    path("hotels/", HotelProfileListView.as_view(), name="hotel-list"),
    path("rooms/create/", RoomCreateView.as_view(), name="room-create"),
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("packages/create/", PackageCreateView.as_view(), name="package-create"),
    path("packages/", PackageListView.as_view(), name="package-list"),
]
