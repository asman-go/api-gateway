from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import logging

from asman.gateway.core.types import (
    AppGatewayConfig,
    Environment,
)
from asman.gateway.middlewares import (
    AdminAuthMiddleware,
    AuthMiddleware,
    ExceptionMiddleware,
    LoggerMiddleware,
)
from asman.gateway.routers import (
    AuthRouter,
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

        def base_app(environment: Environment, logger_name: str) -> FastAPI:
            app = FastAPI(
                debug=True if environment in [Environment.TESTING] else False
            )

            # app.add_middleware(HTTPSRedirectMiddleware)
            app.add_middleware(LoggerMiddleware, app_name=logger_name)
            app.add_middleware(ExceptionMiddleware, app_name=logger_name)

            app.include_router(DevChecksRouter)

            return app

        app = base_app(self.environment, self.logger_name)

        admin_app = base_app(self.environment, self.logger_name)
        admin_app.add_middleware(AdminAuthMiddleware, app_name=self.logger_name)
        admin_app.include_router(AuthRouter, prefix='/auth')

        user_app = base_app(self.environment, self.logger_name)
        # Пока проверки на API_KEY нет
        user_app.add_middleware(AuthMiddleware, app_name=self.logger_name)
        user_app.include_router(ProgramRouter, prefix='/program')
        user_app.include_router(ExampleRouter, prefix='/example')

        app.mount('/app', user_app)
        app.mount('/admin', admin_app)

        return app
