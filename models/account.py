from budget import db
from models.payment import Payment

__author__ = 'true'


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    info = db.Column(db.String(256))
    creation_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payments = db.relationship('Payment', backref='accounts',
                               lazy='dynamic', cascade="all, delete-orphan")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'creation_date': self.creation_date,
            'user_id': self.user_id,
            'payments': [a.serialize() for a in self.payments.all()]
        }
