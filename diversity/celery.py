import os
from datetime import datetime

from django.conf import settings

from celery import Celery
from celery.schedules import crontab


p = os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diversity.settings')

app = Celery('diversity')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(result_expires=3600, enable_utc=True, timezone='UTC')

app.conf.beat_schedule = {
    'update_info': {
        'task': 'main_app.tasks.update_info',
        'schedule': crontab(minute=0, hour='*/3')
    }
}