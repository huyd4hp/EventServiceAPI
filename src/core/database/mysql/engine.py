from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists,create_database
from core import settings
Engine = create_engine(f"mysql+pymysql://{settings.MYSQL_USERNAME}:rootMYSQL@localhost:3307/EventManagement")
if not database_exists(Engine.url):
    create_database(Engine.url)