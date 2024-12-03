import logging
import uvicorn
import sys

from asman.core.adapters.clients.facebook import FacebookConfig
from asman.gateway.core.types import Environment
from asman.gateway.apps.api import GatewayAPI
from asman.gateway.core.configs import (
    ApiGatewayConfig,
    ApiKeyConfig,
    AppGatewayConfig,
)


config = ApiGatewayConfig()  # from envs

app_config = AppGatewayConfig(
    environment=config.ENVIRONMENT,
    logger_name=config.API_GATEWAY_LOGGER_NAME,

    api_secrets=ApiKeyConfig(),
    fb_secrets=FacebookConfig(),
)

# Настройка логгера
logging.basicConfig(
    level=logging.DEBUG if config.ENVIRONMENT == Environment.TESTING else logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

gateway = GatewayAPI(app_config).start()


if __name__ == '__main__':
    uvicorn.run(
        gateway,
        host=config.HTTP_HOST,
        port=config.API_GATEWAY_HTTP_PORT,
    )
