from django.contrib import admin
from django.urls import include, path

urlpatterns = [
   path('admin/', admin.site.urls),
   path('accounts/', include('accounts.urls')),
   path('listings/', include('listings.urls')),
   path('chat/', include('chat.urls')),
   path('booking/', include('booking.urls')),
   path('reviews/', include('reviews.urls')),
   path('notifications/', include('notifications.urls')),
]
