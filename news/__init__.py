from .celery import app as celery_app

from newsapp.tasks import get_news

__all__ = ("celery_app",)
