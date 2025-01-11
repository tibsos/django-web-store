from django.db import models as m

from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

from uuid import uuid4

class Card(m.Model):

    uid = m.UUIDField(primary_key=True, default=uuid4, editable=False)

    profile = m.ForeignKey('Profile', on_delete = m.DO_NOTHING, blank = True, null = True)

    card_number = m.CharField(max_length = 19)
    expiry_date = m.CharField(max_length = 5)
    cvv = m.CharField(max_length = 3)

    created_at = m.DateTimeField(auto_now_add = True)

    def __str__(self):

        return self.profile.name



class Profile(m.Model):

    uid = m.UUIDField(primary_key=True, default=uuid4, editable=False)

    user = m.OneToOneField(User, on_delete = m.CASCADE, related_name = 'profile')

    name = m.CharField(max_length = 100)
    phone = m.TextField(null = True)

    password_recovery_token = m.TextField(blank = True, null = True)

    def __str__(self):
        
        return self.user.username

    class Meta:

        ordering = ['-name']

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:

        Profile.objects.create(user = instance)