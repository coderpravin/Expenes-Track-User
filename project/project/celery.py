import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

#celery app
app =  Celery('project')

#load setting from djago
app.config_from_object('django.conf:settings', namespace='CELERY')

#task discovery
app.autodiscover_tasks()
