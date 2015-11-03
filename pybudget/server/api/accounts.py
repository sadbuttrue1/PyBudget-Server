import datetime
from os import abort

from flask import request, jsonify, url_for, g

from pybudget.server.budget import app, db
from pybudget.server.budget import auth
from pybudget.server.models.account import Account

__author__ = 'true'


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
    if not account or account.user_id != g.user.id:
        abort(404)
    if name is not None:
        account.name = name
    if info is not None:
        account.info = info
    db.session.commit()

    return jsonify({'name': account.name}), 201, {'Location': url_for('get_account', id=account.id)}


@app.route('/api/accounts/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_account(id):
    account = Account.query.get(id)
    if not account or account.user_id != g.user.id:
        abort(404)
    db.session.delete(account)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/accounts/<int:id>')
@auth.login_required
def get_account(id):
    account = Account.query.get(id)
    if not account or account.user_id != g.user.id:
        abort(404)
    return jsonify(account.serialize())


@app.route('/api/accounts', methods=['GET'])
@auth.login_required
def get_accounts():
    return jsonify(accounts=[a.serialize() for a in g.user.accounts.all()])
