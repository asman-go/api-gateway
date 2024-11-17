from fastapi import APIRouter, Body, Response
from typing import Annotated, List

from asman.core.adapters.clients.facebook import FacebookConfig
from asman.domains.facebook_api.use_cases import (
    SubscribeNewDomainsUseCase,
    UnsubscribeDomainsUseCase,
)

from asman.core.adapters.db import PostgresConfig


router = APIRouter()

"""
Задачи:

1. Подписаться на новые события в Certificate Transparency Log для домена
2. Отписаться от новых событий в Certificate Transparency Log для домена
3.

"""

@router.put('/subscribe')
async def subscribe(domains: Annotated[List[str], Body(embed=True)]):
    facebook_config = FacebookConfig()
    postgres_config = PostgresConfig()
    use_case = SubscribeNewDomainsUseCase(facebook_config, postgres_config)

    _domains = await use_case.execute(domains)

    return Response(status_code=200) if _domains else Response(status_code=409)


@router.put('/unsubscribe')
async def unsubscribe(domains: Annotated[List[str], Body(embed=True)]):
    facebook_config = FacebookConfig()
    postgres_config = PostgresConfig()

    use_case = UnsubscribeDomainsUseCase(facebook_config, postgres_config)

    status = await use_case.execute(domains)

    return Response(status_code=200) if status else Response(status_code=409)
