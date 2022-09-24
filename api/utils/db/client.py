import sys

from sqlalchemy.orm import scoped_session, sessionmaker

if __name__ == "__main__":
    # for development
    from master.models.sessions import Sessions
    import base
else:
    # in docker container
    sys.path.append("/app")
    # noinspection PyUnresolvedReferences
    from utils.db.master.models.sessions import Sessions
    # noinspection PyUnresolvedReferences
    from utils.db import base


class SQLClient:
    def __init__(self):
        self.connection = base.create_connection()
        self.SQLSession = scoped_session(
                sessionmaker(
                        bind=self.connection,
                        autocommit=False,
                        autoflush=True
                ))  # type: sqlalchemy.orm.Session
