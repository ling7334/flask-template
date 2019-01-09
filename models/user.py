import string, random, hashlib

from flask_template.app import db
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True)
    salt = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    last_login = db.Column(db.DateTime)

    def __init__(self, username, password, email=None):
        salt = ''.join(random.choice(string.ascii_letters+string.digits) for x in range(32))
        password = hashlib.sha256((password+salt).encode()).hexdigest()
        self.username=username
        self.password=password
        self.salt=salt
        self.email=email

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'username'   : self.username,
           'email'      : self.email,
           'admin'      : self.admin,
           'active'     : self.active,
           'last_login' : self.last_login,
           'created_on' : self.created_on,
           'updated_on' : self.updated_on
       }