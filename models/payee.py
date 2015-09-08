from budget import db

__author__ = 'true'


class Payee(db.Model):
    __tablename__ = 'payees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    info = db.Column(db.String(256))
    creation_date = db.Column(db.DateTime)
    payee_type_id = db.Column(db.Integer, db.ForeignKey('payeetypes.id'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'creation_date': self.creation_date,
            'payee_type_id': self.payee_type_id
        }
