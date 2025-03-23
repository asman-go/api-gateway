from fastapi import APIRouter

from asman.domains.example import (
    ExampleUseCase,
    Request,
    Config,
)


router = APIRouter()


@router.get('/')
async def start():
    use_case = ExampleUseCase(
        Config(some_value='123456')
    )
    request = Request(data='test1')
    response = use_case.execute(request)

    return { "message": response }
