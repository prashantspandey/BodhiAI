import os
from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','bodhiai.settings')

app =Celery('bodhiai',
            backend='redis://h:p5fa2d1747657f37369c546555b5ead7c36d444561db4a48bdeeae7ca705efbb8@ec2-52-201-158-7.compute-1.amazonaws.com:8399',
            broker='amqp://eijjkdor:ho4xHWwK5z81boEeXGatt6RAJu7wG228@termite.rmq.cloudamqp.com/eijjkdor')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

