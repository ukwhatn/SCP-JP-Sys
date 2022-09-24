from __future__ import annotations

import os

import sqlalchemy


def create_engine() -> sqlalchemy.engine.Engine:
    DATABASE = "postgresql"
    USER = "api"
    PASSWORD = "Lqckon!wjLMBmsN!9aZPfuN8c"
    DB_NAME = "master"

    if os.environ.get("PORT_POSTGRES") is None:
        HOST = "localhost"
        PORT = 54002
    else:
        HOST = "postgres"
        PORT = 5432

    CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

    return sqlalchemy.create_engine(CONNECT_STR, echo=False)


def create_connection() -> sqlalchemy.engine.Connection:
    engine = create_engine()
    connection = engine.connect()
    connection.execute("SET search_path TO system")
    return connection
