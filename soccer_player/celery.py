import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soccer_player.settings')

app = Celery('soccer_player')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# TO SCHEDULE TASKS
app.conf.beat_schedule = {
  "count-players-every-30-secs": {
        "task": "players.tasks.count_players",
        "schedule": 30.0
    },
    "update_players_everyday":{
      "task": "players.tasks.update_players_from_json",
      "schedule": crontab(hour=12, minute=53)
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')


app.conf.broker_connection_retry_on_startup = True

