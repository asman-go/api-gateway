import pytest

from fastapi.testclient import TestClient

from asman.core.adapters.tests import facebook_config
from asman.gateway.apps.api import GatewayAPI
from asman.gateway.core.configs import ApiGatewayConfig, ApiKeyConfig, AppGatewayConfig


@pytest.fixture
def postgres_config(monkeypatch):
    monkeypatch.setenv('POSTGRES_DB', 'my_db')
    monkeypatch.setenv('POSTGRES_USER', 'my_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'my_password')
    monkeypatch.setenv('POSTGRES_HOST', 'localhost')
    monkeypatch.setenv('POSTGRES_PORT', '6432')


@pytest.fixture
def api_config(monkeypatch):
    monkeypatch.setenv('HTTP_HOST', 'localhost')
    monkeypatch.setenv('API_GATEWAY_HTTP_PORT', '8080')

    return ApiGatewayConfig()


@pytest.fixture
def api_key_config(monkeypatch):
    monkeypatch.setenv('USER_API_KEY', 'user-api-key')
    monkeypatch.setenv('ADMIN_API_KEY', 'admin-api-key')

    return ApiKeyConfig()


@pytest.fixture
def app_config(api_config, api_key_config, facebook_config):
    return AppGatewayConfig(
        environment=api_config.ENVIRONMENT,
        logger_name=api_config.API_GATEWAY_LOGGER_NAME,
        api_secrets=api_key_config,
        fb_secrets=facebook_config,
    )


@pytest.fixture
def gateway_app(app_config, postgres_config):
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
