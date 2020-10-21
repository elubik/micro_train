from datetime import datetime

from api import db


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    barrier_state = db.Column(db.String(10), unique=False, nullable=False)
    last_update = db.Column(
        db.DateTime, unique=False, nullable=False, default=datetime.utcnow
    )

    def __repr__(self):
        return "<Station %r>" % self.name
