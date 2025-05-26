from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.types import ASGIApp
import typing
import logging


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, dispatch: typing.Optional[DispatchFunction] = None, app_name: str = "", api_key: str = "") -> None:
        super().__init__(app, dispatch)
        self.API_KEY = api_key
        self.logger = logging.getLogger(app_name)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # self.logger.debug(request)
        auth_cookie = request.cookies.get('session')
        auth_header = request.headers.get('Authorization')

        auth_factor = auth_cookie if auth_cookie else auth_header

        # TODO: запуск use-case на проверку API_KEY, пока static
        # Как проверять не по всем путям?

        if not auth_factor or auth_factor != self.API_KEY:
            return Response(status_code=401)

        response = await call_next(request)

        # self.logger.debug(response)

        return response