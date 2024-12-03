from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from starlette.types import ASGIApp
import typing
import logging


class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, dispatch: typing.Optional[DispatchFunction] = None, app_name: str = "") -> None:
        super().__init__(app, dispatch)
        self.logger = logging.getLogger(app_name)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        self.logger.info(f'Request: {request.method} {request.url} {request.headers.items()}')

        if request.method in ('POST', 'PUT', 'PATCH'):
            body = await request.body()
            self.logger.info(f'Request body ({request.url.path}): {body.decode("utf-8")}')

        response = await call_next(request)

        # https://stackoverflow.com/questions/71882419/fastapi-how-to-get-the-response-body-in-middleware
        self.logger.info(
            f'Request is processed: {request.method} {request.url} '
            f'Status is {response.status_code}'
        )

        return response
