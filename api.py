import datetime
from flask import request, jsonify, url_for, g
from flask.ext.restful import abort
from sqlalchemy.exc import SQLAlchemyError
from budget import app, db, auth
from models import User, Account

__author__ = 'true'


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
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
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


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


@app.route('/api/accounts', methods=['POST'])
@auth.login_required
def new_account():
    name = request.json.get('name')
    info = request.json.get('info')
    if name is None:
        abort(400)
    account = Account(name=name, info=info, creation_date=datetime.datetime.now(), user_id=g.user.id)
    db.session.add(account)
    db.session.commit()

    return jsonify({'name': account.name}), 201, {'Location': url_for('get_account', id=account.id)}


@app.route('/api/accounts/<int:id>', methods=['PUT'])
@auth.login_required
def update_account(id):
    name = request.json.get('name')
    info = request.json.get('info')
    account = Account.query.get(id)
    if name is not None:
        account.name = name
    if info is not None:
        account.info = info
    db.session.commit()

    return jsonify({'name': account.name}), 201, {'Location': url_for('get_account', id=account.id)}


@app.route('/api/accounts/<int:id>')
@auth.login_required
def get_account(id):
    account = Account.query.get(id)
    if not account:
        abort(400)
    return jsonify(id=account.id, name=account.name, info=account.info, creation_date=account.creation_date,
                   user_id=account.user_id)
