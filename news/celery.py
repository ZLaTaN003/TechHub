import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
app = Celery("news")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'test': {
        'task': 'newsapp.tasks.get_news',
        'schedule': crontab(minute=15,hour=18),
    },
    'delete': {
         'task': 'newsapp.tasks.clean_db',
         'schedule': crontab(0,0,day_of_month=1,month_of_year=4)
    }

}

app.conf.timezone = 'Asia/Calcutta'
