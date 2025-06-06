from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import logging

from asman.gateway.core.configs import AppGatewayConfig
from asman.gateway.core.types import Environment
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
    # FacebookWebhookRouter,
    # CertificateTransparencyRouter,
)
from asman.gateway.web import WebApp


class GatewayAPI(object):
    config: AppGatewayConfig
    logger: logging.Logger

    def __init__(self, config: AppGatewayConfig) -> None:
        self.config = config
        self.logger = logging.getLogger(config.logger_name)

    def start(self) -> FastAPI:

        app = self._base_fast_api_app(self.config.logger_name)
        # app.root_path = '/api'

        app.mount('/api/public', self._public_api(self.config.logger_name))
        app.mount('/api/integrations', self._integrations_api(self.config.logger_name))

        app.mount('/api/admin', self._admin_api(self.config.logger_name))
        app.mount('/api/private', self._private_api(self.config.logger_name))

        app.mount('/', WebApp)

        return app

    def _admin_api(self, app_name: str) -> FastAPI:

        admin_app = self._base_fast_api_app(app_name)

        admin_app.add_middleware(AdminAuthMiddleware, app_name=app_name, api_key=self.config.api_secrets.ADMIN_API_KEY)
        admin_app.include_router(AuthRouter, prefix='/auth')

        return admin_app

    def _private_api(self, app_name: str) -> FastAPI:

        user_app = self._base_fast_api_app(app_name)

        user_app.add_middleware(AuthMiddleware, app_name=app_name, api_key=self.config.api_secrets.USER_API_KEY)
        user_app.include_router(ProgramRouter, prefix='/program')
        user_app.include_router(ExampleRouter, prefix='/example')
        # user_app.include_router(CertificateTransparencyRouter, prefix='/ctlog')

        return user_app

    def _public_api(self, app_name: str) -> FastAPI:

        public_api = self._base_fast_api_app(app_name)
        public_api.include_router(DevChecksRouter)

        return public_api

    def _integrations_api(self, app_name: str) -> FastAPI:

        integrations_app = self._base_fast_api_app(app_name)
        # integrations_app.include_router(FacebookWebhookRouter, prefix='/fb')

        return integrations_app

    def _base_fast_api_app(self, app_name: str) -> FastAPI:
        app = FastAPI(
            debug=True if self.config.environment in [Environment.TESTING] else False
        )

        # app.add_middleware(HTTPSRedirectMiddleware)
        app.add_middleware(LoggerMiddleware, app_name=app_name)
        app.add_middleware(ExceptionMiddleware, app_name=app_name)

        return app
