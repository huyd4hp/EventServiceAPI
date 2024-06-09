import os
from dotenv import load_dotenv
load_dotenv()

class Settings():
    APP_TITLE = os.getenv("APP_TITLE")
    APP_VERSION = os.getenv("APP_VERSION","1.0.0") 
    APP_PORT = int(os.getenv("APP_PORT",7000)) 
    APP_DEBUG = os.getenv("APP_DEBUG","True") == "True" 
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    REFRESH_KEY = os.getenv("REFRESH_KEY")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS","localhost:9092")
    
settings = Settings()