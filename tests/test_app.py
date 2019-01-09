import os
import tempfile
import pytest

from flask_template.app import create_app


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
    flask_template.config['TESTING'] = True
    client = flask_template.test_client()

    yield client

    os.close(db_fd)
    os.unlink(db_link)

def test_index(client):
    rv = client.get('/')
    assert b'hello world' in rv.data