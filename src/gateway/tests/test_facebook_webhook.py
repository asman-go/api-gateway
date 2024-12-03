import pytest

import json
from asman.gateway.core.utils import hmac_digest
from asman.domains.facebook_api.api import FacebookCtEvent, NewCertificateEvent


FACEBOOK_WEBHOOK_PATH = '/fb/webhook'


@pytest.fixture
def fb_ct_event():
    return FacebookCtEvent(
        object='certificate_transparency',
        entry=[
            NewCertificateEvent(
                id='123',
                time=123,
                changes={
                    'value': {
                        'certificate_pem': 'TBD2'  # TODO: пример серта создать
                    }
                }
            )
        ],
    )


def test_check_facebook_webhook(integrations_client, facebook_config):
    CHALLENGE = '12345'
    response = integrations_client.get(
        FACEBOOK_WEBHOOK_PATH,
        params={
            'hub.challenge': CHALLENGE,
            'hub.mode': 'test',
            'hub.verify_token': facebook_config.FACEBOOK_WEBHOOK_VERIFICATION_TOKEN,
        }
    )

    assert response.status_code == 200
    assert response.text == CHALLENGE
    # assert response.json() == {
    #     'statusCode': 200,
    #     'body': CHALLENGE,
    # }

    response = integrations_client.get(
        FACEBOOK_WEBHOOK_PATH,
        params={
            'hub.challenge': CHALLENGE,
            'hub.mode': 'test',
            'hub.verify_token': 'BAD' + facebook_config.FACEBOOK_WEBHOOK_VERIFICATION_TOKEN,
        }
    )

    assert response.status_code == 401


def te1st_new_facebook_ct_event(integrations_client, facebook_config):
    body = json.dumps({'key': 'value'})
    response = integrations_client.post(
        FACEBOOK_WEBHOOK_PATH,
        headers={
            'Content-Type': 'application/json',
            'X-Hub-Signature-256': hmac_digest(
                facebook_config.FACEBOOK_CLIENT_SECRET,
                body,
            ),
        },
        content=body.encode(),
    )

    assert response.status_code == 200

    response = integrations_client.post(
        FACEBOOK_WEBHOOK_PATH,
        headers={
            'Content-Type': 'application/json',
            'X-Hub-Signature-256': 'BAD_SIGNATURE',
        },
        data=body,
    )

    assert response.status_code == 401
