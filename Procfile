web: gunicorn bodhiai.wsgi  
worker: celery -A bodhiai worker  --without-heartbeat --without-gossip --without-mingle -l info

