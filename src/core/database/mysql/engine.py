from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists,create_database

Engine = create_engine("mysql+pymysql://root:rootMYSQL@localhost:3307/EventManagement")
if not database_exists(Engine.url):
    create_database(Engine.url)