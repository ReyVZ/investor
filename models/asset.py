from datetime import datetime
from db import db


class AssetModel(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(
        'UserModel', backref=db.backref('user', lazy=True))

    def __init__(self, ticker, price, count, user_id, dt=None):
        self.ticker = ticker
        self.price = price
        self.count = count
        self.dt = dt
        self.user_id = user_id

    def json(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'price': self.price,
            'count': self.count,
            'dt': self.dt.strftime('%d.%m.%Y'),
            'user_id': self.user_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
