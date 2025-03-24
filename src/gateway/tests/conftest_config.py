import pytest

from asman.gateway.core.configs import ApiGatewayConfig, ApiKeyConfig, AppGatewayConfig


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
