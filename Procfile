web: gunicorn django_crowdfund.wsgi --log-file -
worker: celery worker -B -A django_crowdfund -l info