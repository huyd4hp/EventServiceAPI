from fastapi import Header
from api.response import HTTP_403_FORBIDDEN
import jwt 
from core.settings import settings

def ManagementUser(Authorization:str=Header()):
    payload = jwt.decode(Authorization,settings.ACCESS_KEY,algorithms=['HS256'])
    if payload.get("role") == "User":
        raise HTTP_403_FORBIDDEN("Not Enough Permissions")
    return payload

def User(Authorization:str=Header()):
    payload = jwt.decode(Authorization,settings.ACCESS_KEY,algorithms=['HS256'])
    return payload