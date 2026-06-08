from django.urls import path
from .views import GuideProfileCreateView, GuideProfileListView

urlpatterns = [
    path("guides/create/", GuideProfileCreateView.as_view(), name="guide-create"),
    path("guides/", GuideProfileListView.as_view(), name="guide-list"),
]