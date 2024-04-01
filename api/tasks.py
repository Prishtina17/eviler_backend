import django
from celery import shared_task

from eviler.celery import app
from .models import ActiveSession
@shared_task
def delete_expired_sessions(*args):
    active_sessions = ActiveSession.objects.all()
    for session in active_sessions:
        if session.expiration < django.utils.timezone.now():
            session.delete()
