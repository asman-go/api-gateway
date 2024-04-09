from pydantic_settings import BaseSettings

from asman.gateway.core.types import Environment


class ApiGatewayConfig(BaseSettings):
    API_GATEWAY_LOGGER_NAME: str = 'gateway'
    ENVIRONMENT: Environment = Environment.TESTING
    HTTP_HOST: str = '0.0.0.0'
    API_GATEWAY_HTTP_PORT: int = 3000
