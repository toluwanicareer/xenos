from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
	passport=models.ImageField(null=True)
	phone=models.CharField(null=True, max_length=200)
	wallet=models.IntegerField(null=True)





@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)