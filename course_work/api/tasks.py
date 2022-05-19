from celery import shared_task
from django.db import transaction

from core.models import Bb, Notification


@shared_task
def send_notification(viewed_by_id, bb_id):
    bb = Bb.objects.get(pk=bb_id)
    with transaction.atomic():
        bb.views += 1
        bb.save()
        Notification.objects.create(master=bb.author, viewed_by_id=viewed_by_id, bb=bb)
