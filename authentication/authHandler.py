import time, os
import jwt
from dotenv import load_dotenv

load_dotenv(".env")

JWT_SECRET = os.environ["SECRET"]
JWT_ALGORITHM = os.environ["ALGORITHM"]


def tokenResponse(token: str):
    return {
        "acccess token": token
    }


# Func for Signing JWT string
def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiration": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return tokenResponse(token)


def decodeJWT(token: str):
    try:
        decodeToken = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decodeToken if decodeToken['expiration'] >= time.time() else None
    except:
        return {}
