import pytest

from fastapi.testclient import TestClient

from asman.gateway.apps.api import GatewayAPI
from asman.gateway.core.configs import ApiGatewayConfig
from asman.gateway.core.types import AppGatewayConfig


@pytest.fixture
def api_config():
    return ApiGatewayConfig(
        HTTP_HOST='localhost',
        API_GATEWAY_HTTP_PORT=8080,
    )


@pytest.fixture
def app_config(api_config):
    return AppGatewayConfig(
        environment=api_config.ENVIRONMENT,
        logger_name=api_config.API_GATEWAY_LOGGER_NAME,
    )


@pytest.fixture
def client(app_config):
    return TestClient(
        GatewayAPI(app_config).start()
    )
