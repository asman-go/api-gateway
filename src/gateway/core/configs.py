from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings
import uuid

from asman.gateway.core.types import Environment
from asman.core.adapters.clients.facebook import FacebookConfig


class ApiGatewayConfig(BaseSettings):
    API_GATEWAY_LOGGER_NAME: str = Field(default='gateway')
    ENVIRONMENT: Environment = Field(default=Environment.TESTING)
    HTTP_HOST: str = Field(default='0.0.0.0')
    API_GATEWAY_HTTP_PORT: int = Field(default=3000)


class ApiKeyConfig(BaseSettings):
    USER_API_KEY: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ADMIN_API_KEY: str = Field(default_factory=lambda: str(uuid.uuid4()))


class AppGatewayConfig(BaseModel):
    environment: Environment
    logger_name: str

    api_secrets: ApiKeyConfig
    fb_secrets: FacebookConfig
