from enum import Enum
from pydantic import BaseModel


class Environment(Enum):
    PRODUCTION = "production"
    TESTING = "testing"


class AppGatewayConfig(BaseModel):
    environment: Environment
    logger_name: str
