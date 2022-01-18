from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, LoginManager

db= SQLAlchemy()
login= LoginManager()

class UserModel(UserMixin, db.Model):
    __tablename__= 'users'

    id= db.Column(db.Integer, primary_key= True)
    email= db.Column(db.String(80), unique= True)
    username= db.Column(db.String(100), unique= True)
    password_hash= db.Column(db.String())

    def set_password(self,password):
        self.password_hash= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.id

class Todo(db.Model):
    __tablename__= 'tasks'

    id= db.Column(db.Integer, primary_key=True)
    content= db.Column(db.String(200), nullable= False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow())
    date_finished= db.Column(db.DateTime, default= datetime.utcnow())
    is_finished= db.Column(db.Boolean, default= False)
    is_pvt= db.Column(db.Boolean, default= False)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user= db.relationship("UserModel", backref="tasks")

    def __repr__(self):
        return '<Task %r>' % self.id

@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))