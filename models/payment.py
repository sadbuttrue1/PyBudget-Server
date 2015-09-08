from budget import db

__author__ = 'true'


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    info = db.Column(db.String(256))
    creation_date = db.Column(db.DateTime)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    payee_id = db.Column(db.Integer, db.ForeignKey('payees.id'))
    cleared = db.Column(db.Boolean)
    cleared_date = db.Column(db.DateTime)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'creation_date': self.creation_date,
            'account_id': self.account_id,
            'payee_id': self.payee_id,
            'cleared': self.cleared,
            'cleared_date': self.cleared_date
        }
