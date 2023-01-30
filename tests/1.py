import sys
sys.path.append('..')
from sqlalchemy import text
from importlib import reload
from config import Config


'''Создание тестовой базы данных'''
Config.DATABASE_URL = 'postgresql://postgres:password@localhost:5433'
import models as _models
try:
    with _models.engine.connect() as connection:
        connection.execute(text("COMMIT"))
        connection.execute(text('CREATE DATABASE test'))
except Exception as err:
    print(err)
Config.DATABASE_URL = 'postgresql://postgres:password@localhost:5433/test'
_models = reload(_models)

'''Создание таблиц в базе test '''
_models.Base.metadata.create_all(bind=_models.engine)
with _models.engine.connect() as connection:
    connection.execute(text("COMMIT"))
    connection.execute(text('DELETE FROM menu;DELETE FROM submenu;DELETE FROM dish;'))
