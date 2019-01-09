import os, string, random, datetime

from flask import Flask, jsonify, session, g
from flask_sqlalchemy import SQLAlchemy

from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '''<%(asctime)s> - [%(levelname)s] @ '%(pathname)s:%(lineno)d': %(message)s''',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,
    instance_path=os.path.dirname(__file__),
    instance_relative_config=True)

    from util.CustomJSONEncoder import CustomJSONEncoder
    app.json_encoder = CustomJSONEncoder

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_json("developemnt.json")
        app.config.update(SECRET_KEY=''.join(random.choice(string.ascii_letters+string.digits) for x in range(128)))
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        app.config.update(SECRET_KEY=''.join(random.choice(string.ascii_letters+string.digits) for x in range(128)))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    with app.app_context():
        from models import (User, Session)
        db.create_all()

    @app.before_request
    def before_request():
        if 'user' not in g:
            if 'user_token' in session:
                try:
                    user_session = db.session.query(Session).filter_by(session_key=session['user_token']).first()
                    if user_session.expire_at > datetime.datetime.now():
                        g.user = user_session.user
                except:
                    app.logger.exception("Could not find user")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
        g.pop('user', None)
        # app.logger.info("appcontext closed")

    import example
    app.add_url_rule('/', 'index', example.index)
    app.add_url_rule('/login', view_func=example.LoginAPI.as_view('login'))
    app.add_url_rule('/logout', view_func=example.LogoutAPI.as_view('logout'))

    import admin
    app.register_blueprint(admin.adminBlueprint, url_prefix='/admin')

    return app