from flask import request, jsonify, g, url_for
from flask.ext.restful import abort
from sqlalchemy.exc import SQLAlchemyError

from pybudget.server.budget import app, db, auth
from pybudget.server.models.user import User

__author__ = 'true'


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        reason = str(e)
        print(reason)
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id)}


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    return jsonify({'username': user.username})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
