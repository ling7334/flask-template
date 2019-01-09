import traceback

from flask import jsonify, current_app, request
from flask.views import MethodView
from flask_template.app import db
from models import User

from util.decorators import admin_required

class UserAPI(MethodView):

    decorators = [admin_required]

    def get(self):
        arg_id = request.args.get('id')
        arg_username = request.args.get('username')
        arg_email = request.args.get('email')
        if arg_id:
            user = db.session.query(User).filter_by(id=arg_id).first()
        elif arg_username:
            user = db.session.query(User).filter_by(username=arg_username).first()
        elif arg_email:
            user = db.session.query(User).filter_by(email=arg_email).first()
        else:
            current_app.logger.warn("ArgumnetError: %s", request.args)
            return jsonify({
                'code': 'ArgumnetError',
                'msg': 'At least one of (id, username, email) should be supplied.'
            }), 400
        if user:
            current_app.logger.info("User founded: %s", user)
            return jsonify({
                'code': 'Success',
                'msg': 'User founded.',
                'data': user.serialize
            })
        current_app.logger.warn("User not founded: %s", request.args)
        return jsonify({
            'code': 'NotFound',
            'msg': 'User not founded.',
        }), 404

    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        new_user = User(username, password, email)
        try:
            db.session.add(new_user)
            db.session.commit()
            current_app.logger.info("new user added: %s", new_user)
            return jsonify({
                'code': 'Success',
                'msg': 'Account created.'
            }), 201
        except Exception as err:
            current_app.logger.exception("Unexpected error.")
            return jsonify({
                "code": err.__class__.__name__,
                "msg": "Fail to create account.",
                "data": err._message()
            }), 500

    def delete(self):
        arg_id = request.json.get('id')
        arg_username = request.json.get('username')
        arg_email = request.json.get('email')
        if arg_id:
            user = db.session.query(User).filter_by(id=arg_id).first()
        elif arg_username:
            user = db.session.query(User).filter_by(username=arg_username).first()
        elif arg_email:
            user = db.session.query(User).filter_by(email=arg_email).first()
        else:
            current_app.logger.warn("ArgumnetError: %s", request.args)
            return jsonify({
                'code': 'ArgumnetError',
                'msg': 'At least one of (id, username, email) should be supplied.'
            }), 400
        if user:
            db.session.delete(user)
            db.session.commit()
            current_app.logger.info("User deleted: %s", user)
            return jsonify({
                'code': 'Success',
                'msg': 'User deleted.',
                'data': user.serialize
            }), 204
        current_app.logger.warn("User not founded: %s", request.args)
        return jsonify({
            'code': 'NotFound',
            'msg': 'User not founded.',
        }), 404
