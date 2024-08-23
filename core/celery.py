import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings',namespace='CELERY')



app.conf.beat_schedule = {
    'birthday-wish':{
        'task':'delivery.tasks.brithday_wish',
        'schedule': crontab(minute='*')
    }
    }

app.autodiscover_tasks()
