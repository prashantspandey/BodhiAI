web: gunicorn bodhiai.wsgi  --timeout 120 --log-level debug
worker: celery -A bodhiai worker  --without-heartbeat --without-gossip --without-mingle -l info

