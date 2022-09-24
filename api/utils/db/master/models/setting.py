import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE = "postgresql"
HOST = "localhost"
PORT = 54002
USER = "api"
PASSWORD = "Lqckon!wjLMBmsN!9aZPfuN8c"
DB_NAME = "master"

CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

# Engine の作成
Engine = create_engine(
        CONNECT_STR,
        encoding="utf-8",
        echo=False
)

Base = declarative_base()
