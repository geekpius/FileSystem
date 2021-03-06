from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch  import receiver
from .models import UserImage, User


@receiver(post_save, sender=User)
def create_user_image(sender, instance, created, **kwargs):
    if created:
        UserImage.objects.create(user=instance)
