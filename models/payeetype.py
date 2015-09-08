from budget import db

__author__ = 'true'


class PayeeType(db.Model):
    __tablename__ = 'payeetypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    info = db.Column(db.String(256))
    creation_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payees = db.relationship('Payee', backref='payeetypes',
                             lazy='dynamic', cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'creation_date': self.creation_date,
            'user_id': self.user_id,
            'payees': [a.serialize() for a in self.payees.all()]
        }
