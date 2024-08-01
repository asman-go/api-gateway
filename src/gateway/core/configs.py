from pydantic import Field
from pydantic_settings import BaseSettings
import uuid

from asman.gateway.core.types import Environment


class ApiGatewayConfig(BaseSettings):
    API_GATEWAY_LOGGER_NAME: str = 'gateway'
    ENVIRONMENT: Environment = Environment.TESTING
    HTTP_HOST: str = '0.0.0.0'
    API_GATEWAY_HTTP_PORT: int = 3000


class ApiKeyConfig(BaseSettings):
    MASTER_API_KEY: str = Field(default_factory=lambda: uuid.uuid4())


class FacebookConfig(BaseSettings):
    FACEBOOK_WEBHOOK_VERIFICATION_TOKEN: str = 'UNDEFINED'
    FACEBOOK_CLIENT_SECRET: str = 'UNDEFINED'
