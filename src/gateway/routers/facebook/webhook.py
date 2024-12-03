from fastapi import APIRouter, Query, Header, Request, Response
import pydantic
from typing import Annotated
import json

from asman.gateway.core.utils import hmac_digest
from asman.domains.facebook_api.use_cases import NewCtEventUseCase
from asman.domains.facebook_api.api import FacebookCtEvent
from asman.core.adapters.db import PostgresConfig
from asman.core.adapters.clients.facebook import FacebookConfig


router = APIRouter()

"""
Задачи:

1. Получать информацию о новых доменах из Facebook CT Log
2. 

"""


@router.get('/webhook')
async def webhook(
            challenge: Annotated[str, Query(alias='hub.challenge')],
            mode: Annotated[str, Query(alias='hub.mode')],
            verify_token: Annotated[str, Query(alias='hub.verify_token')]
        ):
    config = FacebookConfig()
    print(
        'Receive Webhook Verification Request. hub.mode is',
        mode,
        # config.FACEBOOK_WEBHOOK_VERIFICATION_TOKEN,
        'challenge is',
        challenge
    )

    if verify_token == config.FACEBOOK_WEBHOOK_VERIFICATION_TOKEN:
        return Response(status_code=200, content=challenge, media_type='text/plain')

    return Response(status_code=401)


@router.post('/webhook')
async def new_ct_event(
            signature: Annotated[str, Header(alias='X-Hub-Signature-256')],
            request: Request,
        ):
    facebook_config = FacebookConfig()
    postgres_config = PostgresConfig()

    body = (await request.body()).decode()
    # print('signature:', hmac_digest(facebook_config.FACEBOOK_CLIENT_SECRET, body))
    if signature.split('=')[1] == hmac_digest(facebook_config.FACEBOOK_CLIENT_SECRET, body):
        print('FB WebHook body event (TODO):', body)
        ct_event = pydantic.TypeAdapter(
            FacebookCtEvent
        ).validate_python(
            json.loads(body)
        )

        print('FB WebHook parsed event (TODO):', ct_event)
        use_case = NewCtEventUseCase(None, postgres_config)
        status = await use_case.execute(ct_event)

        return Response(status_code=200) if status else Response(status_code=502)

    return Response(status_code=401)
