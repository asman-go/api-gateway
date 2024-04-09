from fastapi import APIRouter

from asman.domains.example import (
    ExampleUseCase,
    Request,
)

from asman.core.adapters.db import DynamoDBConfig

router = APIRouter()

@router.get('/')
async def start():
    config = DynamoDBConfig()
    use_case = ExampleUseCase(None, config)
    request = Request(data='test1')
    response = use_case.execute(request)

    return { "message": response }
