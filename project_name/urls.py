from django.contrib import admin
from django.urls import include, path

# ADD THESE TWO
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('listings/', include('listings.urls')),
    path('chat/', include('chat.urls')),
    path('booking/', include('booking.urls')),
    path('reviews/', include('reviews.urls')),
    path('notifications/', include('notifications.urls')),
]


# ADD THIS AT THE VERY BOTTOM
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )