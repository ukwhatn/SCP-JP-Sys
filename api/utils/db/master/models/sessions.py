import datetime
import sys

import sqlalchemy

# for alembic script
sys.path.append("./master/models")
sys.path.append("/app/utils/db/master/models")
from setting import Base


class Sessions(Base):
    __tablename__ = "sessions"
    __table_args__ = {"schema": "system", "extend_existing": True}

    session = sqlalchemy.Column(sqlalchemy.String, primary_key=True, )
    data = sqlalchemy.Column(sqlalchemy.JSON(none_as_null=True), nullable=True, )
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now(), nullable=False)

