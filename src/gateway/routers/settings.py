from fastapi import APIRouter, Body

router = APIRouter()

"""
Задачи:

1. Дать возможность изменять настройки отдельных компонентов,
без перезапуска и перераскатки Asman Compute Engine
2. Возможно, в некоторых случаях и дин секретов

"""

@router.get('/')
async def all():
    return [{
        'key': 'dynproperty key',
        'value': 'dynproperty value',
    }]


@router.put('/')
async def set_dynproperty():
    return {
        'key': 'dynproperty key',
        'value': 'dynproperty value',
    }


@router.get('/secrets')
async def secrets():
    return [{
        'key': 'secret dynproperty key'
    }]


@router.put('/secrets')
async def set_secret_dynproperty():
    return {
        'key': 'secret dynproperty key'
    }
