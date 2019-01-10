import os
import json
import tempfile
import datetime
import pytest

from flask_template.app import (create_app, db)
from models import (User, Session)


@pytest.fixture
def client():
    db_fd, db_link = tempfile.mkstemp()
    flask_template = create_app({
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///' + os.path.abspath(db_link),
        "SQLALCHEMY_TRACK_MODIFICATIONS":False,
        "DATABASE_CONNECT_OPTIONS":{},
        "THREADS_PER_PAGE":2,
        "CSRF_ENABLED":True,
        "CSRF_SESSION_KEY":"session"
    })

    with flask_template.app_context():
        admin = User('admin','admin','admin@flask-template.com')
        admin.admin = True
        admin.active = True
        user = User('user','user','user@flask-template.com')
        user.active = True
        inactive_user = User('inactiveuser','inactiveuser','inactiveuser@flask-template.com')
        db.session.add(admin)
        db.session.add(user)
        db.session.add(inactive_user)
        db.session.commit()

    flask_template.config['TESTING'] = True
    client = flask_template.test_client()

    yield client

    os.close(db_fd)
    os.unlink(db_link)

def login(client, username, password):
    return client.post('/login', json={
        'username': username,
        'password': password
    }, follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_index(client):
    rv = client.get('/')
    assert b'hello world' == rv.data

def test_login_logout(client):
    """Make sure login and logout works."""

    rv = login(client, 'admin', 'admin')
    assert '200 OK' == rv.status
    body = rv.get_json()
    assert 'Success' == body['code']
    assert 'Successfully login.' == body['msg']

    rv = logout(client)
    assert '200 OK' == rv.status
    body = rv.get_json()
    assert 'Success' == body['code']
    assert 'Successfully logout.' == body['msg']

    rv = logout(client)
    assert '401 UNAUTHORIZED' == rv.status

    rv = login(client, 'admin', 'wrongpassword')
    assert '400 BAD REQUEST' == rv.status
    body = rv.get_json()
    assert 'LoginFailed' == body['code']
    assert 'Incorrect username or password.' == body['msg']

    rv = login(client, 'wrongusername', 'wrongpassword')
    assert '400 BAD REQUEST' == rv.status
    body = rv.get_json()
    assert 'LoginFailed' == body['code']
    assert 'Incorrect username or password.' == body['msg']

    rv = login(client, 'inactiveuser', 'inactiveuser')
    assert '400 BAD REQUEST' == rv.status
    body = rv.get_json()
    assert 'LoginFailed' == body['code']
    assert 'User is inactive.' == body['msg']