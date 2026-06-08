from django.urls import include, path
from . import views

urlpatterns = [
   path('admin/', admin.site.urls),
   path('accounts/', include('accounts.urls')),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:id>/', views.property_detail, name='property_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]