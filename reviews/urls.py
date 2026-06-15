from django.urls import path
from .views import GuideReviewCreateView, GuideReviewListView, HotelReviewCreateView, HotelReviewListView


urlpatterns = [
    path("guides/", GuideReviewCreateView.as_view(), name="guide-review-create"),
    path("guides/list/", GuideReviewListView.as_view(), name="guide-review-list"),   
    path("hotels/", HotelReviewCreateView.as_view(), name="hotel-review-create"),
    path("hotels/list/", HotelReviewListView.as_view(), name="hotel-review-list"),
]