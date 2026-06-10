from django.contrib import admin
from .models import GuideProfile, HotelProfile, Package, Room
# Register your models here.
admin.site.register(GuideProfile)
admin.site.register(HotelProfile)
admin.site.register(Room)
admin.site.register(Package)