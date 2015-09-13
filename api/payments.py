import datetime
from flask import request, jsonify, url_for, g
from flask.ext.restful import abort
from budget import app, db
from budget import auth
from models.payment import Payment
from models.user import User

__author__ = 'true'


@app.route('/api/payments', methods=['POST'])
@auth.login_required
def new_payment():
    name = request.json.get('name')
    info = request.json.get('info')
    account_id = request.json.get('account_id')
    payee_id = request.json.get('payee_id')
    cleared = request.json.get('cleared')
    cleared_date = request.json.get('cleared_date')
    if name is None:
        abort(400)
    # TODO check that current user owns account and payee
    if account_id is None:
        abort(400)
    if payee_id is None:
        abort(400)
    if cleared is None and cleared_date is None:
        abort(400)
    payment = Payment(name=name, info=info, creation_date=datetime.datetime.now(), account_id=account_id,
                      payee_id=payee_id, cleared=cleared, cleared_date=datetime.datetime.utcfromtimestamp(cleared_date))
    db.session.add(payment)
    db.session.commit()

    return jsonify({'name': payment.name}), 201, {'Location': url_for('get_payment', id=payment.id)}


@app.route('/api/payments/<int:id>', methods=['PUT'])
@auth.login_required
def update_payment(id):
    name = request.json.get('name')
    info = request.json.get('info')
    account_id = request.json.get('account_id')
    payee_id = request.json.get('payee_id')
    cleared = request.json.get('cleared')
    cleared_date = request.json.get('cleared_date')
    payment = Payment.query.get(id)
    if not payment:
        abort(404)
    if name is not None:
        payment.name = name
    if info is not None:
        payment.info = info
    if account_id is not None:
        payment.account_id = account_id
    if payee_id is not None:
        payment.payee_id = payee_id
    if cleared is not None:
        payment.cleared = cleared
    if cleared_date is not None:
        payment.cleared_date = datetime.datetime.utcfromtimestamp(cleared_date)
    db.session.commit()

    return jsonify({'name': payment.name}), 201, {'Location': url_for('get_payment', id=payment.id)}


@app.route('/api/payments/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_payment(id):
    payment = Payment.query.get(id)
    if not payment:
        abort(404)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/api/payments/<int:id>')
@auth.login_required
def get_payment(id):
    payment = Payment.query.get(id)
    if not payment:
        abort(404)
    return jsonify(payment.serialize())


@app.route('/api/payments', methods=['GET'])
@auth.login_required
def get_payments():
    payments = []
    for a in g.user.accounts.all():
        for p in a.payments.all():
            payments.append(p)
    return jsonify(payments=[a.serialize() for a in payments])
