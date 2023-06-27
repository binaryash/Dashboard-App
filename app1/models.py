from datetime import datetime
from app1 import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.Date, nullable=True)
    completion_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id
    


