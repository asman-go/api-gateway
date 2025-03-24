import pytest
from fastapi.testclient import TestClient

from asman.gateway.apps.api import GatewayAPI


@pytest.fixture
def gateway_app(app_config, init_postgres_envs, init_dynamodb_envs):
    return GatewayAPI(app_config).start()


@pytest.fixture
def private_client(gateway_app, app_config):
    client = TestClient(
        gateway_app,
        headers={
            'Authorization': app_config.api_secrets.USER_API_KEY,
        },
    )
    client.base_url = client.base_url.join('/api/private')

    return client


@pytest.fixture
def admin_client(gateway_app, app_config):
    client = TestClient(
        gateway_app,
        headers={
            'Authorization': app_config.api_secrets.ADMIN_API_KEY,
        },
    )
    client.base_url = client.base_url.join('/api/admin')

    return client


@pytest.fixture
def public_client(gateway_app):
    client = TestClient(
        gateway_app,
    )
    client.base_url = client.base_url.join('/api/public')

    return client


@pytest.fixture
def integrations_client(gateway_app):
    client = TestClient(
        gateway_app,
    )
    client.base_url = client.base_url.join('/api/integrations')

    return client
