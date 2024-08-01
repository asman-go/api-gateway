from fastapi import APIRouter, Body

router = APIRouter()

"""
Задачи:

1. Динамически добавлять и удалять API-ключи для доступа к Asman Compute Engine
2. Это может сделать только владелец по своему "master" API_KEY

"""

@router.get('/')
async def all():
    return [
        'API_KEY_NAME_1',
        'API_KEY_NAME_2',
    ]


@router.post('/')
async def add():
    return {
        'status': 'OK'
    }


@router.delete('/')
async def delete():
    return {
        'status': 'OK'
    }
