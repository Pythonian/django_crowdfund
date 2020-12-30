web: gunicorn django_crowdfund.wsgi --log-file -
worker: celery -A django_crowdfund worker -l info