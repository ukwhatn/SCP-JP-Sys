import sys
import secrets

sys.path.append("/app/utils/db/")
from client import SQLClient
from master.models.sessions import Sessions

from sqlalchemy.orm import Session as SASession
from datetime import datetime, timedelta


class SessionControler:
    def __init__(self):
        self.sqlsession = SQLClient().SQLSession()  # type: SASession

    def get_session(self, session_id: str):
        non_expired_limit = datetime.now() - timedelta(hours=1)
        search = self.sqlsession.query(Sessions).filter_by(session=session_id).filter(Sessions.updated_at > non_expired_limit).first()
        if search is None:
            return None
        self.sqlsession.execute("UPDATE system.sessions SET updated_at = :now WHERE session = :session", {"now": datetime.now(), "session": session_id})
        self.sqlsession.commit()
        search = self.sqlsession.query(Sessions).filter_by(session=session_id).filter(Sessions.updated_at > non_expired_limit).first()
        return search

    def create_session_id(self):
        session_id = secrets.token_urlsafe(32)
        self.sqlsession.add(Sessions(session=session_id))
        self.sqlsession.commit()
        return session_id

    def start_session(self, session_id: str = None):
        if session_id is None:
            session_id = self.create_session_id()
        session = self.get_session(session_id)
        if session is None:
            return None
        return UserSession(session.session, session.data, session.created_at, session.updated_at)


class UserSession:
    def __init__(self, session: str, data: dict, created_at: datetime, updated_at: datetime):
        self.session = session
        self.data = data
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "session": self.session,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }