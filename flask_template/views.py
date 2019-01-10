import hashlib, datetime
from flask import jsonify, request, session, current_app
from flask.views import MethodView

from flask_template.app import db
from models import User, Session
from util.decorators import user_required

def Index():
    return 'hello world'


class LoginAPI(MethodView):

    def post(self):
        try:
            arg_username = request.json['username']
            arg_password = request.json['password']
        except:
            current_app.logger.warn("ArgumnetError: %s", request.args)
            return jsonify({
                'code': 'ArgumnetError',
                'msg': 'username and password must be supplied.'
            }), 400
        user = db.session.query(User).filter_by(username=arg_username).first()
        if not user:
            current_app.logger.warn("User not founded: %s", request.args)
            return jsonify({
                'code': 'LoginFailed',
                'msg': 'Incorrect username or password.',
            }), 400
        hash_password = hashlib.sha256((arg_password+user.salt).encode()).hexdigest()
        if hash_password != user.password:
            current_app.logger.warn("Incorrect password: %s", request.args)
            return jsonify({
                'code': 'LoginFailed',
                'msg': 'Incorrect username or password.',
            }), 400
        if not user.active:
            current_app.logger.warn("Inactive user: %s", user)
            return jsonify({
                'code': 'LoginFailed',
                'msg': 'User is inactive.',
            }), 400
        # Delete all session this user used before
        db.session.query(Session).filter_by(user_id=user.id).delete()
        NOW = datetime.datetime.now()
        session_key = hashlib.sha256((str(user.id) + user.username + str(NOW.timestamp())).encode()).hexdigest()
        user_session = Session(session_key,user.id)
        user.last_login=NOW
        db.session.add(user_session)
        db.session.commit()
        session['user_token'] = session_key
        current_app.logger.info("New session created: %s", session_key)
        return jsonify({
            'code': 'Success',
            'msg': 'Successfully login.',
        })

class LogoutAPI(MethodView):

    decorators = [user_required]

    def get(self):
        user_token = session.pop('user_token')
        if user_token:
            user_session = db.session.query(Session).filter_by(session_key=user_token).first()
            user_session.expire_at = datetime.datetime.now()
            db.session.commit()
            return jsonify({
                'code': 'Success',
                'msg': 'Successfully logout.',
            })
        return jsonify({
            'code': 'LogoutFailed',
            'msg': 'Invalid token.',
        }), 400