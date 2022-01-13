from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db= SQLAlchemy()

class Todo(db.Model):
    __tablename__= 'tasks'

    id= db.Column(db.Integer, primary_key=True)
    content= db.Column(db.String(200), nullable= False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow())
    date_finished= db.Column(db.DateTime, default= datetime.utcnow())
    is_finished= db.Column(db.Boolean, default= False)

    def __repr__(self):
        return '<Task %r>' % self.id