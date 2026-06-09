from django.urls import path
from .views import GuideProfileCreateView, GuideProfileListView, HotelProfileCreateView, HotelProfileListView

urlpatterns = [
    path("guides/create/", GuideProfileCreateView.as_view(), name="guide-create"),
    path("guides/", GuideProfileListView.as_view(), name="guide-list"),
    path("hotels/create/", HotelProfileCreateView.as_view(), name="hotel-create"),
    path("hotels/", HotelProfileListView.as_view(), name="hotel-list"),
]
