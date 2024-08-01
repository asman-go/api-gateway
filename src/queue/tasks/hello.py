from celery import shared_task


@shared_task
def hello(to):
    return 'hello {0}'.format(to)
