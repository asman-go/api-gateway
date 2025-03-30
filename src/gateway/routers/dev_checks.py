from fastapi import APIRouter
from asman.tasks.common import PingTask


router = APIRouter()

@router.get('/healthcheck')
async def healthcheck():
    return { "message": "OK" }


@router.get('/celery')
async def celery_ping():
    result = PingTask.delay()
    return {'message': result.get()}
