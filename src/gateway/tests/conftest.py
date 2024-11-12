import pytest

from fastapi.testclient import TestClient

from asman.gateway.apps.api import GatewayAPI
from asman.gateway.core.configs import ApiGatewayConfig, ApiKeyConfig, FacebookConfig, AppGatewayConfig


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
def facebook_webhook_config(monkeypatch):
    monkeypatch.setenv('FACEBOOK_CLIENT_SECRET', 'client-secret')
    monkeypatch.setenv('FACEBOOK_WEBHOOK_VERIFICATION_TOKEN', 'verification-token')

    return FacebookConfig()


@pytest.fixture
def app_config(api_config, api_key_config, facebook_webhook_config):
    return AppGatewayConfig(
        environment=api_config.ENVIRONMENT,
        logger_name=api_config.API_GATEWAY_LOGGER_NAME,
        api_secrets=api_key_config,
        fb_secrets=facebook_webhook_config,
    )


@pytest.fixture
def gateway_app(app_config):
    return GatewayAPI(app_config).start()


@pytest.fixture
def user_client(gateway_app, app_config):
    return TestClient(
        gateway_app,
        root_path='/app',
        headers={
            'Authorization': app_config.api_secrets.USER_API_KEY,
        },
    )


@pytest.fixture
def admin_client(gateway_app, app_config):
    return TestClient(
        gateway_app,
        root_path='/admin',
        headers={
            'Authorization': app_config.api_secrets.ADMIN_API_KEY,
        },
    )


@pytest.fixture
def public_client(gateway_app):
    return TestClient(
        gateway_app,
    )
