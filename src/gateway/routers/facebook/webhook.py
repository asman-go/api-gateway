from fastapi import APIRouter, Query, Header, Request
from typing import Annotated

from asman.gateway.core.configs import FacebookConfig
from asman.gateway.core.utils import hmac_digest


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
    print('Receive Webhook Verification Request. hub.mode is', mode)

    if verify_token == config.FACEBOOK_WEBHOOK_VERIFICATION_TOKEN:
        return {
            'statusCode': 200,
            'body': challenge
        }

    return {
        'statusCode': 200,
        'body': ''
    }


@router.post('/webhook')
async def new_ct_event(
            signature: Annotated[str, Header(alias='X-Hub-Signature-256')],
            request: Request,
        ):
    config = FacebookConfig()
    body = await request.body()
    if signature == hmac_digest(config.FACEBOOK_CLIENT_SECRET, body):
        ...
