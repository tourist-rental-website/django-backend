from django.urls import path
from .views import GuideProfileCreateView

urlpatterns = [
    path("guides/", GuideProfileCreateView.as_view(), name="guide-create"),
]