import pytest

import json
from asman.gateway.core.utils import hmac_digest
from asman.domains.facebook_api.api import FacebookCtEvent, NewCertificateEvent


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
                        'certificate_pem': 'TODO'  # TODO: пример серта создать
                    }
                }
            )
        ],
    )


def test_check_facebook_webhook(public_client, facebook_webhook_config):
    CHALLENGE = '12345'
    response = public_client.get(
        '/integrations/fb/webhook',
        params={
            'hub.challenge': CHALLENGE,
            'hub.mode': 'test',
            'hub.verify_token': facebook_webhook_config.FACEBOOK_WEBHOOK_VERIFICATION_TOKEN,
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        'statusCode': 200,
        'body': CHALLENGE,
    }

    response = public_client.get(
        '/integrations/fb/webhook',
        params={
            'hub.challenge': CHALLENGE,
            'hub.mode': 'test',
            'hub.verify_token': 'BAD' + facebook_webhook_config.FACEBOOK_WEBHOOK_VERIFICATION_TOKEN,
        }
    )

    assert response.status_code == 401


def te1st_new_facebook_ct_event(public_client, facebook_webhook_config):
    body = json.dumps({'key': 'value'})
    response = public_client.post(
        '/integrations/fb/webhook',
        headers={
            'Content-Type': 'application/json',
            'X-Hub-Signature-256': hmac_digest(
                facebook_webhook_config.FACEBOOK_CLIENT_SECRET,
                body,
            ),
        },
        content=body.encode(),
    )

    assert response.status_code == 200

    response = public_client.post(
        '/integrations/fb/webhook',
        headers={
            'Content-Type': 'application/json',
            'X-Hub-Signature-256': 'BAD_SIGNATURE',
        },
        data=body,
    )

    assert response.status_code == 401
