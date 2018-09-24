import os
from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','bodhiai.settings')

app =\
        Celery('bodhiai',backend='redis://h:pe972ab554e541ecd6e49dce5357f0071db5ba80136abb3825d3fbae21b66eb07@ec2-34-201-229-104.compute-1.amazonaws.com:7759',broker='amqp://eijjkdor:ho4xHWwK5z81boEeXGatt6RAJu7wG228@termite.rmq.cloudamqp.com/eijjkdor')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

