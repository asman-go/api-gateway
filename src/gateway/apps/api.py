from fastapi import FastAPI
import logging

from asman.gateway.core.types import (
    AppGatewayConfig,
    Environment,
)
from asman.gateway.middlewares import (
    ExceptionMiddleware,
    LoggerMiddleware,
)
from asman.gateway.routers import (
    ProgramRouter,
    DevChecksRouter,
    ExampleRouter,
)


class GatewayAPI(object):
    environment: Environment
    logger_name: str
    logger: logging.Logger

    def __init__(self, config: AppGatewayConfig) -> None:
        self.environment = config.environment
        self.logger_name = config.logger_name
        self.logger = logging.getLogger(self.logger_name)

    def start(self) -> FastAPI:

        app = FastAPI(
            debug=True if self.environment in [Environment.TESTING] else False
        )

        app.add_middleware(LoggerMiddleware, app_name=self.logger_name)
        app.add_middleware(ExceptionMiddleware, app_name=self.logger_name)

        app.include_router(DevChecksRouter)
        app.include_router(ProgramRouter, prefix='/program')
        app.include_router(ExampleRouter, prefix='/example')

        return app
