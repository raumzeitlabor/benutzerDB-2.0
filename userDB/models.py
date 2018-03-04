from django.db import models
from django.db.models.signals import post_save, pre_save

from django.contrib.auth.models import User

from django.dispatch import receiver

import random


class Profile(models.Model):
    """Stores additional user information.

    Every User has a Profile attached that stores extra information. While we
    could also extend the User model, this is overkill for our use case.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Whether or not this User is a member of the RaumZeitLabor e.V. This must
    # only be settable by administrators (the NOC) or board members (the
    # Vorstand).
    member = models.BooleanField(default=False, blank=True)
    # The PIN for accessing the room. This must be a 6 digit number.
    pin = models.PositiveSmallIntegerField(null=True)


# When a User is a member, automatically generate a random 6-digit PIN if there
# is none yet.
@receiver(pre_save, sender=Profile)
def create_pin(sender, instance, **kwargs):
    if instance.member and not instance.pin:
        instance.pin = random.randint(10**5, (10**6)-1)


# Whenever a User object is created, create a Profile for it.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Whenever a User object is modified, also save its Profile.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
