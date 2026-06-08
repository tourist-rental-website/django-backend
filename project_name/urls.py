from django.contrib import admin
from django.urls import include, path

urlpatterns = [
<<<<<<< HEAD
   path('admin/', admin.site.urls),
   path('accounts/', include('accounts.urls')),
=======
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('listings/', include('listings.urls')),
>>>>>>> a808dac (feat listing page added)
]
