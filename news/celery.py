import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
app = Celery("news")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'test': {
        'task': 'newsapp.tasks.news_data',
        'schedule': crontab(minute=9,hour=12),
    },
    # 'delete': {
    #      'task': 'newsapp.tasks.clean_db',
    #      'schedule': crontab(0,0,day_of_month=1,month_of_year=4)
    # },
    'product': {
         'task': 'newsapp.tasks.products_data',
         'schedule': crontab(minute=9,hour=12)
    }

}

app.conf.timezone = 'Asia/Kolkata'
