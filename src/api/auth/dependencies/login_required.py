from fastapi import Header
import jwt as JWT
from api.response import HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from core.database.redis import RedisClient
# dependency
async def login_required(Authorization:str = Header()):       
    try:
        _,Session_ID = RedisClient.get_session(Authorization)
        if Session_ID is None:
            raise HTTP_401_UNAUTHORIZED("Expired Session Error")
    except JWT.ExpiredSignatureError:
        raise HTTP_401_UNAUTHORIZED("Expired Signature Error")
    except JWT.InvalidTokenError:
        raise HTTP_401_UNAUTHORIZED("Invalid Token Error")
    except Exception as e:
        raise HTTP_500_INTERNAL_SERVER_ERROR(e)