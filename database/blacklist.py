from sqlalchemy import Column, String, UnicodeText
from database import SESSION, BASE


class BlackList(BASE):
    __tablename__ = "blacklist"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(UnicodeText)

    def __init__(self, chat_id, reason):
        self.chat_id = str(chat_id)  # ensure string
        self.reason = reason

    def __repr__(self):
        return "<BL %s>" % self.chat_id


BlackList.__table__.create(checkfirst=True)


def is_bl(chat_id: int):
    try:
        bl = SESSION.query(BlackList).get(str(chat_id))
        if bl:
            return bl
        return None
    finally:
        SESSION.close()


def blacklist(chat_id: int, reason=None):
    if is_bl(chat_id) is None:
        user = BlackList(str(chat_id), reason)
        SESSION.add(user)
        SESSION.commit()


def unblacklist(chat_id: int):
    user = is_bl(chat_id)
    if user:
        SESSION.delete(user)
        SESSION.commit()
