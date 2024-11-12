import uvicorn
from asman.gateway.apps.api import GatewayAPI
from asman.gateway.core.configs import (
    ApiGatewayConfig,
    FacebookConfig,
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

gateway = GatewayAPI(app_config).start()


if __name__ == '__main__':
    uvicorn.run(
        gateway,
        host=config.HTTP_HOST,
        port=config.API_GATEWAY_HTTP_PORT,
    )
