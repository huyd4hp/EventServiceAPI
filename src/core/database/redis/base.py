import redis
from threading import Lock
import jwt
from core.settings import settings

class Redis:
    _instances = {}
    _lock = Lock()

    def __new__(cls, host='localhost', port=6379, db=0, *args, **kwargs):
        key = f"{host}:{port}:{db}"
        with cls._lock:
            if key not in cls._instances:
                instance = super(Redis, cls).__new__(cls)
                instance._initialized = False
                cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, host='localhost', port=6379, db=0):
        if not self._initialized:
            self._client = redis.Redis(host=host, port=port, db=db)
            self._initialized = True

    def get_session(self, token: str):
        Client_ID = Session_ID = None
        payload = jwt.decode(token, settings.ACCESS_KEY, algorithms=['HS256'])
        Client_ID = payload.get("_id")
        Session_ID = self._client.get(Client_ID)
        return Client_ID, Session_ID

    def set(self, key, value):
        self._client.set(key, value)

    def delete(self,key):
        self._client.delete(key)

    def get(self,key):
        return self._client.get(key).decode()

    @property
    def client(self):
        return self._client

# Khởi tạo hai instances với các cấu hình khác nhau
RedisSesion = Redis(port=8100)
RedisBooking = Redis(port=8111)
