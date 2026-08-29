from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import UserTaskProgress


@receiver(post_save, sender=UserTaskProgress)
def update_completed_at(sender, instance, **kwargs):
    if instance.is_completed and instance.completed_at is None:
        instance.completed_at = timezone.now()
        instance.save(update_fields=['completed_at'])

    elif not instance.is_completed and instance.completed_at is not None:
        instance.completed_at = None
        instance.save(update_fields=['completed_at'])