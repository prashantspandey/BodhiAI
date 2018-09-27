import os
from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','bodhiai.settings')

app =\
        Celery('bodhiai',backend='redis://h:pe972ab554e541ecd6e49dce5357f0071db5ba80136abb3825d3fbae21b66eb07@ec2-34-201-229-104.compute-1.amazonaws.com:7759',broker='amqp://hcqbbswt:YDIbEj8WB5P04o9D-rR3y2J65weLBie0@clam.rmq.cloudamqp.com/hcqbbswt')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

