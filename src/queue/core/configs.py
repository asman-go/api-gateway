from pydantic import BaseModel
from pydantic_settings import BaseSettings


class CeleryConfig(BaseModel):
    enable_utc: bool = True
    timezone: str = 'Europe/London'


class BackendConfig(BaseSettings):
    ...


class BrokerConfig(BaseSettings):
    ...
