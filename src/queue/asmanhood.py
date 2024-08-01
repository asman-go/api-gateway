from celery import Celery

from asman.queue.core.configs import CeleryConfig
from asman.queue.tasks import HelloTask


# python -m celery -A asmanhood worker --loglevel=info
app = Celery(
    'asmanhood',  # Базовое название модуля для тасков, должно совпадать с названием файла, но не с названием пакетов ...
    broker='redis://localhost',  # docker run -d -p 6379:6379 redis
    backend='redis://localhost',
)

app.config_from_object(CeleryConfig)
app.conf.update(
    # result_backend='redis://localhost',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)
# app.autodiscover_tasks()


# @app.task
# def hello(to):
#     return f'Hello, {to}'


if __name__ == '__main__':
    # app.tasks.register(HelloTask())

    result = HelloTask.delay('Ike')
    print(f'Task result: {result.get()}')
