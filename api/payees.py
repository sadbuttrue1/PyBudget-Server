import datetime
from flask import request, jsonify, url_for, g
from flask.ext.restful import abort
from budget import app, auth, db
from models.payee import Payee

__author__ = 'true'


@app.route('/api/payees', methods=['POST'])
@auth.login_required
def new_payee():
    name = request.json.get('name')
    info = request.json.get('info')
    payee_type_id = request.json.get('payee_type_id')
    if name is None:
        abort(400)
    if payee_type_id is None:
        abort(400)
    payee = Payee(name=name, info=info, creation_date=datetime.datetime.now(), payee_type_id=payee_type_id)
    db.session.add(payee)
    db.session.commit()

    return jsonify({'name': payee.name}), 201, {'Location': url_for('get_payee', id=payee.id)}


@app.route('/api/payees/<int:id>', methods=['PUT'])
@auth.login_required
def update_payee(id):
    name = request.json.get('name')
    info = request.json.get('info')
    payee_type_id = request.json.get('payee_type_id')
    payee = Payee.query.get(id)
    if not payee:
        abort(404)
    if name is not None:
        payee.name = name
    if info is not None:
        payee.info = info
    if payee_type_id is not None:
        if payee_type_id not in g.user.payeetypes.all():
            abort(404)
        payee.payee_type_id = payee_type_id
    db.session.commit()

    return jsonify({'name': payee.name}), 201, {'Location': url_for('get_payee', id=payee.id)}


@app.route('/api/payees/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_payee(id):
    payee = Payee.query.get(id)
    if not payee or payee.payee_type_id not in g.user.payeetypes.all():
        abort(404)
    db.session.delete(payee)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/payees/<int:id>')
@auth.login_required
def get_payee(id):
    payee = Payee.query.get(id)
    if not payee or payee.payee_type_id not in g.user.payeetypes.all():
        abort(404)
    return jsonify(payee.serialize())


@app.route('/api/payees', methods=['GET'])
@auth.login_required
def get_payees():
    payees = []
    for t in g.user.payeetypes.all():
        for p in t.payees.all():
            payees.append(p)
    return jsonify(payees=[a.serialize() for a in payees])
