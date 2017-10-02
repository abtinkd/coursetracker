from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    university = models.CharField(max_length = 100, default = '')
    interests = models.CharField(max_length = 500 , default='')

def makeProfile(sender, **kwargs):
    # if the user has been created
    if kwargs['created']:
        # associate this current user with a user profile
        userProfile = UserProfile.objects.create(user = kwargs['instance'])

# when a user is created and saved, the make profile function is trigered
post_save.connect(makeProfile, sender = User  )