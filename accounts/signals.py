from django.db.models.signals import post_save
from django.contrib.auth.models import User
from listings.models import *

def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'guide':
            GuideProfile.objects.create(
                user = instance,

            )
            print('Traveler profile created')

post_save.connect(create_profile,sender = User)