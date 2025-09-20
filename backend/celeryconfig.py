from celery.schedules import crontab
from datetime import timedelta

CELERY_IMPORTS = ('utils.process_worker')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'process_order': {
        'task': 'utils.process_worker.process_order',
        'schedule': timedelta(seconds=3)
    },
    'update_profit_history': {
        'task': 'utils.process_worker.update_profit_history',
        'schedule': timedelta(seconds=10)
    }
}
