# Import a post_save signal when a user is created
from django.db.models.signals import post_save, post_delete
# Import the built-in User model, which is a sender
from django.contrib.auth.models import User
from django.dispatch import receiver  # Import the receiver
from .models import Profile, Question
from django.db.models import F


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Question)
def incrementTotal(sender, created, **kwargs):
    if created:
        for profile in Profile.objects.all():
            profile.total_questions += 1
            profile.save()


@receiver(post_delete, sender=Question)
def decrementTotal(sender, **kwargs):
    Profile.objects.all().update(total_questionstions=F('total_questions') - 1)
