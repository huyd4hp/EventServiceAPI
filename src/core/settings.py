import os
from .vault import VaultClient

def LoadConfig(MODE:str = "DEBUG"):
    vaultInstance = VaultClient(
        VAULT_HOST= "127.0.0.1" if MODE == "DEBUG" else os.getenv("VAULT_HOST"),
        VAULT_TOKEN= os.getenv("VAULT_TOKEN")
    )   
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    APP_HOST = os.getenv("APP_HOST","127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", 7000))
    # Authentication keys
    ACCESS_KEY = vaultInstance.readSecret("AuthSecret/data/SecretKey")['data']['data']['AccessKey']
    REFRESH_KEY = vaultInstance.readSecret("AuthSecret/data/SecretKey")['data']['data']['RefreshKey']
    # Kafka configuration
    KAFKA_BOOTSTRAP_SERVERS = (
        "127.0.0.1:9092" if MODE == "DEBUG"
        else vaultInstance.readSecret("KafkaBrokers/data/Endpoint")['data']['data']['1']
    )
    # MySQL configuration
    MYSQL_USERNAME = vaultInstance.readSecret("EventService/data/MySQL")['data']['data']['MYSQL_USERNAME']
    MYSQL_ROOT_PASSWORD = vaultInstance.readSecret("EventService/data/MySQL")['data']['data']['MYSQL_ROOT_PASSWORD']
    MYSQL_DATABASE = vaultInstance.readSecret("EventService/data/MySQL")['data']['data']['MYSQL_DATABASE']
    MYSQL_HOST = (
        "127.0.0.1" if MODE == "DEBUG"
        else vaultInstance.readSecret("EventService/data/MySQL")['data']['data']['MYSQL_HOST']
    )
    MYSQL_PORT = vaultInstance.readSecret("EventService/data/MySQL")['data']['data']['MYSQL_PORT']
    # MinIO configuration
    MINIO_HOST = (
        "127.0.0.1" if MODE == "DEBUG"
        else vaultInstance.readSecret("EventService/data/MinIO")['data']['data']['MINIO_HOST']
    )
    MINIO_ACCESS_KEY = vaultInstance.readSecret("EventService/data/MinIO")['data']['data']['MINIO_ACCESS_KEY']
    MINIO_SECRET_KEY = vaultInstance.readSecret("EventService/data/MinIO")['data']['data']['MINIO_SECRET_KEY']
    MINIO_PORT = int(vaultInstance.readSecret("EventService/data/MinIO")['data']['data']['MINIO_PORT'])

    REDIS_SESSION_HOST = (
        "127.0.0.1" if MODE == "DEBUG"
        else vaultInstance.readSecret("AuthSecret/data/Redis")['data']['data']['REDIS_CONNECTION_STRING']
    )
    
    REDIS_BOOKING_HOST = (
        "0.0.0.0" if MODE == "DEBUG"
        else vaultInstance.readSecret("EventService/data/Redis")['data']['data']['REDIS_CONNECTION_STRING']
    )
    
    return (APP_VERSION,APP_PORT,APP_HOST,
    ACCESS_KEY,REFRESH_KEY,
    KAFKA_BOOTSTRAP_SERVERS,
    MYSQL_HOST,MYSQL_PORT,MYSQL_USERNAME,MYSQL_ROOT_PASSWORD,MYSQL_DATABASE,
    MINIO_HOST,MINIO_PORT,MINIO_ACCESS_KEY,MINIO_SECRET_KEY,
    REDIS_BOOKING_HOST,REDIS_SESSION_HOST)
(
    
    APP_VERSION,APP_PORT,APP_HOST,
    ACCESS_KEY,REFRESH_KEY,
    KAFKA_BOOTSTRAP_SERVERS,  
    MYSQL_HOST,MYSQL_PORT,MYSQL_USERNAME,MYSQL_ROOT_PASSWORD,MYSQL_DATABASE,
    MINIO_HOST,MINIO_PORT,MINIO_ACCESS_KEY,MINIO_SECRET_KEY,
    REDIS_BOOKING_HOST,REDIS_SESSION_HOST,
) = LoadConfig(os.getenv("APP_MODE","DEBUG"))

print(os.getenv("APP_MODE","DEBUG"))
print(KAFKA_BOOTSTRAP_SERVERS)

    
    