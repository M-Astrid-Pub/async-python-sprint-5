from fastapi import HTTPException, status
from fastapi_jwt import JwtAccessBearerCookie

from settings import app_settings

access_security = JwtAccessBearerCookie(
    secret_key=app_settings.AUTHJWT_SECRET_KEY,
    auto_error=False,
    access_expires_delta=app_settings.AUTHJWT_ACCESS_TOKEN_EXPIRES,
)
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
