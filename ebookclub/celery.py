 #celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebookclub.settings')

app = Celery('ebookclub')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

app.conf.timezone = 'Asia/Kolkata'

app.conf.beat_schedule = {
    'check_subcription_statuses': {
        'task': 'members.tasks.notify_subscription_end',
        'schedule': crontab(hour=0, minute=0),        
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')