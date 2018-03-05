from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from macaddress.fields import MACAddressField
import sshpubkeys
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
    member = models.BooleanField(default=False, blank=True,
                                 verbose_name=_('Member'))

    # The PIN for accessing the room. This must be a 6 digit number.
    pin = models.PositiveSmallIntegerField(
        null=True, verbose_name=_('PIN'),
        help_text=_('Will be automatically generated if user is set as member'))

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user__username']
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


class MACAddress(models.Model):
    """Stores a MAC address for a given host, associated with a user.

    A user can have multiple MAC addresses associated with them.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='mac_address')
    mac = MACAddressField(blank=False)
    hostname = models.CharField(max_length=32)

    def __str__(self):
        return self.profile.user.username

    class Meta:
        ordering = ['profile__user__username']
        verbose_name = _('MAC address')
        verbose_name_plural = _('MAC addresses')


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


class SSHKey(models.Model):
    """Stores an SSH public key that can be used to unlock the door."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='ssh_keys')

    name = models.CharField(max_length=200, verbose_name=_('Name'))
    key = models.TextField(verbose_name=_('SSH key'))
    key_type = models.CharField(max_length=30, verbose_name=_('Key type'))

    hash_md5 = models.CharField(
        max_length=47, verbose_name=_('MD5 hash'),
        help_text=_('Automatically generated hash of the key'))

    def __str__(self):
        return self.hash_md5

    class Meta:
        ordering = ['hash_md5']
        verbose_name = _('SSH key')
        verbose_name_plural = _('SSH keys')


@receiver(pre_save, sender=SSHKey)
def create_pin(sender, instance, **kwargs):
    if not instance.hash_md5 or not instance.key_type:
        ssh = sshpubkeys.SSHKey(instance.key)
        ssh.parse()
        instance.hash_md5 = ssh.hash_md5()[4:]
        instance.key_type = instance.key.strip().split()[0][4:]
