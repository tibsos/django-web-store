from django.db import models as m

from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

from uuid import uuid4

from django.db import models

class Card(m.Model):

    uid = m.UUIDField(primary_key=True, default=uuid4, editable=False)

    profile = m.ForeignKey('Profile', on_delete = m.DO_NOTHING, blank = True, null = True)

    card_number = m.CharField(max_length = 19)
    expiry_date = m.CharField(max_length = 5)
    cvv = m.CharField(max_length = 3)

    created_at = m.DateTimeField(auto_now_add = True)

    def __str__(self):

        return self.profile.name



class Profile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    phone = models.TextField(null=True)
    password_recovery_token = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-name']


@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:

        Profile.objects.create(user = instance)