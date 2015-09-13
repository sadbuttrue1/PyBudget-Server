import datetime
from flask import request, jsonify, url_for, g
from flask.ext.restful import abort
from budget import app, db
from budget import auth
from models.payeetype import PayeeType

__author__ = 'true'


@app.route('/api/payeetypes', methods=['POST'])
@auth.login_required
def new_payee_type():
    name = request.json.get('name')
    info = request.json.get('info')
    user_id = request.json.get('user_id')
    if name is None:
        abort(400)
    if user_id is None:
        abort(400)
    payee_type = PayeeType(name=name, info=info, creation_date=datetime.datetime.now(), user_id=user_id)
    db.session.add(payee_type)
    db.session.commit()

    return jsonify({'name': payee_type.name}), 201, {'Location': url_for('get_payee_type', id=payee_type.id)}


@app.route('/api/payeetypes/<int:id>', methods=['PUT'])
@auth.login_required
def update_payee_type(id):
    name = request.json.get('name')
    info = request.json.get('info')
    payee_type = PayeeType.query.get(id)
    if not payee_type:
        abort(404)
    if name is not None:
        payee_type.name = name
    if info is not None:
        payee_type.info = info
    db.session.commit()

    return jsonify({'name': payee_type.name}), 201, {'Location': url_for('get_payee_type', id=payee_type.id)}


@app.route('/api/payeetypes/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_payee_type(id):
    payee_type = PayeeType.query.get(id)
    if not payee_type:
        abort(404)
    db.session.delete(payee_type)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/payeetypes/<int:id>')
@auth.login_required
def get_payee_type(id):
    payee_type = PayeeType.query.get(id)
    if not payee_type:
        abort(404)
    return jsonify(payee_type.serialize())


@app.route('/api/payeetypes', methods=['GET'])
@auth.login_required
def get_payee_types():
    return jsonify(payee_types=[a.serialize() for a in g.user.payeetypes.all()])
