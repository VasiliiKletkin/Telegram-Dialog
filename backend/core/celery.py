import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', '1')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat Settings

# app.conf.beat_schedule = {

#     "check_active_clients": {
#         "task": "check_active_clients",
#         "schedule": crontab(minute=0, hour=0),
#     },

#     "check_company_subscriptions":{
#         "task": "check_company_subscriptions",
#         "schedule": crontab(minute=0, hour=0),
#     }
# }