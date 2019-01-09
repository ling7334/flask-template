import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'flask-template.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
CSRF_SESSION_KEY = "session"

del os