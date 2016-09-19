from werkzeug.security import generate_password_hash,check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask.ext.login import UserMixin
from  . import login_manager
from flask.ext.login import login_required
app = Flask(__name__)
db = SQLAlchemy(app)
class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    def __repr__(self):
        return '<Role %r>' % self.name
class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    #def __repr__(self):
     #   return '<User %r>' % self.username
    #password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed'

if __name__ == '__main__':
    app.run(debug=True)