import redis
from threading import Lock
import jwt
from core.settings import ACCESS_KEY


class Redis:
    _instances = {}
    _lock = Lock()

    def __new__(cls, host='localhost', port=6379, password=None, db=0, *args, **kwargs):
        key = f"{host}:{port}:{db}"            
        if password:
            key = f"{host}:{port}:{db}:{password}"            
        with cls._lock:
            if key not in cls._instances:
                instance = super(Redis, cls).__new__(cls)
                instance._initialized = False
                cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, host='localhost', port=6379, db=0,password=None):
        if not self._initialized:
            self._client = redis.Redis(host=host, port=port, db=db,password=password)
            self._client.ping()
            print("Connect ",host, "OK")
            self._initialized = True
            

    def get_session(self, token: str):
        Client_ID = Session_ID = None
        payload = jwt.decode(token, ACCESS_KEY, algorithms=['HS256'])
        Client_ID = payload.get("_id")
        Session_ID = self._client.get(Client_ID)
        return Client_ID, Session_ID

    def set(self, key, value):
        self._client.set(key, value)

    def delete(self,key):
        self._client.delete(key)

    def get(self,key):
        return self._client.get(key)

    @property
    def client(self):
        return self._client


RedisSesion = Redis(host="RedisSession",password="rootRedis")
RedisBooking = Redis(host="RedisBooking",password="rootRedis")
