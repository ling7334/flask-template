import datetime
from flask_template.app import db
from flask import current_app

class Session(db.Model):
    __tablename__ = 'session'

    session_key = db.Column(db.String, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", uselist=False)
    expire_at = db.Column(db.DateTime)

    def __init__(self, session_key, user_id, expire_at=None):
        expire_at = expire_at or datetime.datetime.now() + datetime.timedelta(seconds=current_app.config.get("SESSION_EXPIRE_SECONDS",30*24*60*60))
        self.session_key=session_key
        self.user_id=user_id
        self.expire_at=expire_at

    def __repr__(self):
        return f'<Session {self.session_key}>'
