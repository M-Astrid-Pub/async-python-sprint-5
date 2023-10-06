from ipaddress import ip_network

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware


class BlacklistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, blacklist: list[str]) -> None:
        super().__init__(app)
        self.app = app
        self.blacklist = [ip_network(subnet) for subnet in blacklist]

    async def dispatch(self, request: Request, call_next: callable):
        client_ip = request.client.host

        if ip_network(client_ip) in self.blacklist:
            return PlainTextResponse("Access denied", status_code=403)

        response = await call_next(request)
        return response
