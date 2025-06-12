from celery import Celery
from celery.signals import task_success

import asman.tasks.common
import asman.tasks.recon

# from asman.tasks.common import DebugTask, HelloTask
from asman.background import CeleryConfig, AppConfig


class MyCelery(Celery):
    def __init__(self, *args, **kwargs):
        self.Task = asman.tasks.common.DebugTask
        super().__init__(*args, **kwargs)


app_config = AppConfig()
celery_config = CeleryConfig()


BACKGROUND_ARGS = [
    'worker',
    '--loglevel=INFO',
    # '--loglevel=DEBUG',
    '-E',  # monitor events for flower
    '-B',  # celery beat for periodic tasks
]

BACKGROUND_APP = MyCelery(
    app_config.name,
    broker=celery_config.broker_url,
    backend=celery_config.result_backend,
)
BACKGROUND_APP.config_from_object(celery_config.model_dump())
BACKGROUND_APP.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': celery_config.result_backend,
        'default_timeout': 60 * 60,
    }
}
BACKGROUND_APP.autodiscover_tasks([
    'asman.tasks',
])


@BACKGROUND_APP.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
    # sender.add_periodic_task(5.0, HelloTask.s('Ike-5'), name='eat every 5')
    ...

@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    print(f'Task {sender.name} succeeded with result: {result}')


if __name__ == '__main__':
    print('Celery app', BACKGROUND_APP)
    # Run worker
    BACKGROUND_APP.worker_main(argv=BACKGROUND_ARGS)

    result1 = asman.tasks.common.HelloTask.delay('Ike')
    print(f'Task result: {result1.get()}')
