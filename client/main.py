from typing import Type, Mapping, no_type_check
import uplink
from requests import Session

from asman.gateway.core.utils import hmac_digest


def parse_response(response_model: Type):
    @uplink.response_handler()
    def _parse_as_pydantic_model(response):
        if response.status_code == 200:
            # TODO: parse response
            return response
        else:
            # TODO: parse error
            return response

    return _parse_as_pydantic_model


class GatewayClient(uplink.Consumer):
    @parse_response(Mapping)
    @uplink.get('/api/healthcheck')
    def _ping(
        self,
    ):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.get('/api/integrations/fb/webhook')
    def facebook_webhook_verify(
        self,
        *,
        challenge: uplink.Query(name='hub.challenge', type=str),
        mode: uplink.Query(name='hub.mode', type=str),
        verify_token: uplink.Query(name='hub.verify_token', type=str),
    ):...

    @no_type_check
    @parse_response(Mapping)
    @uplink.post('/api/integrations/fb/webhook')
    def _facebook_ct_event_send(
        self,
        *,
        signature: uplink.Header(name='X-Hub-Signature-256', type=str),
        body: uplink.Body(type=str),
    ):...

    def ping(self):
        return self._ping()

    def facebook_ct_event_send(self, facebook_secret: str, body: str):
        return self._facebook_ct_event_send(
            signature=hmac_digest(facebook_secret, body),
            body=body,
        )


if __name__ == '__main__':
    session = Session()
    session.headers.update({'Authorization': 'user-api-key'})

    user_client = GatewayClient(
        'http://localhost:7860',
        client=session,
    )
    public_client = GatewayClient(
        'http://localhost:7860',
    )

    print('GET /healthcheck', public_client.ping())
    print('GET /integrations/fb/webhook', public_client.facebook_webhook_verify(challenge='mychallenge', mode='test', verify_token='UNDEFINED'))
    print('POST /integrations/fb/webhook', public_client.facebook_ct_event_send(facebook_secret='UNDEFINED', body='{"event":"test"}'))
