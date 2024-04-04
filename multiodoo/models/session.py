import pickle
from os import environ

from redis import Redis

import odoo
from odoo.http import Application, Session
from odoo.service import security
from odoo.tools import config, lazy_property
from odoo.tools._vendor.sessions import SessionStore


class PickableSession(Session):
    """Specialized Session to avoid endless recursion when pickling."""

    def __getstate__(self):
        slots = {slot: getattr(self, slot) for slot in Session.__slots__}
        return slots, self.__data

    def __setstate__(self, state):
        for key, value in state[0].items():
            setattr(self, key, value)
        self.__data = state[1]


class RedisSessionStore(SessionStore):
    def __init__(self, uri: str):
        super().__init__()
        self.redis = Redis.from_url(uri)
        self.session_class = PickableSession

    def save(self, session: Session):
        self.redis.set(session.sid, pickle.dumps(session))

    def get(self, sid: str) -> Session:
        data = self.redis.get(sid)
        if not data:
            return self.new()

        return pickle.loads(data)

    def delete(self, sid: str) -> None:
        self.redis.delete(sid)

    def rotate(self, session, env):
        self.delete(session.sid)
        session.sid = self.generate_key()
        if session.uid and env:
            session.session_token = security.compute_session_token(session, env)
        session.should_rotate = False
        self.save(session)


def redis_session_gc(_session_store: RedisSessionStore):
    pass


class MultiOdooApplication(Application):
    @lazy_property
    def session_store(self):
        return RedisSessionStore(environ.get("ODOO_REDIS_URL") or config.get("redis_url"))


odoo.http.root = MultiOdooApplication()
odoo.http.session_gc = redis_session_gc
