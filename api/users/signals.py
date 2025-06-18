# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_user_creation_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome to LeadOne',
            f'Hi {instance.name}, your username is {instance.email} and your password is "goated".',
            'noreply@leadone.com',
            [instance.email]
        )
