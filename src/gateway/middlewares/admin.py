from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.types import ASGIApp
import typing
import logging


class AdminAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, dispatch: typing.Optional[DispatchFunction] = None, app_name: str = "", api_key: str = "") -> None:
        super().__init__(app, dispatch)
        self.API_KEY = api_key
        self.logger = logging.getLogger(app_name)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # self.logger.debug(request)

        if request.headers.get('Authorization') != self.API_KEY:
            return Response(status_code=401)

        response = await call_next(request)

        # self.logger.debug(response)

        return response
