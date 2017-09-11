from django.db import models
from django.db.models.signals import post_save, pre_save

from django.contrib.auth.models import User

from django.dispatch import receiver

import random


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member = models.BooleanField(default=False, blank=True)
    pin = models.PositiveSmallIntegerField(null=True)

@receiver(pre_save, sender=Profile)
def create_pin(sender, instance, **kwargs):
    if instance.member and not instance.pin:
        instance.pin = random.randint(0, 10**6)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
