from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from authentication.authHandler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, autoError: bool = True):
        super(jwtBearer, self).__init__(auto_error=autoError)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme!")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired Token!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authprization Token!")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False  # A false flag

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return  isTokenValid