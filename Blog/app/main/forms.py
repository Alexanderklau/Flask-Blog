from flask import Flask
from flask import render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask import session,redirect,url_for,flash
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.mail import Message
from threading import Thread
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['FLASKY_MATL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MATL_SENDER'] = 'Flasky Admin <flasky@example.com>'
app.config["FLASKY_ADMIN"] = os.environ.get('FLASKY_ADMIN')
db = SQLAlchemy(app)
bootstrp = Bootstrap(app)
moment = Moment(app)
def send_email(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MATL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MATL_SENDER'],recipients=[to])
    msg.body =render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr
def send_async_email(app,msg):
    with app.app_context():
        mail = Message()
        mail.send(msg)
class NameForm(Form):
    name = StringField('What is your neme?',validators=[Required()])
    submit = SubmitField('Submit')
class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    def __repr__(self):
        return '<Role %r>' % self.name
    users = db.relationship('User',backref='role')
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    def __repr__(self):
        return '<User %r>' % self.username
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),400
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['Known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User',
                           'mail/new_user',user=user)
            else:
                session['Known'] = True
            session['name'] = form.name.data

        #old_name = session.get('name')
        #if old_name is not None and old_name != form.name.data:
         #   flash('Looks like you have changed your name!')
        #session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',
         form = form,name = session.get('name'),
                           known = session.get('known',False))


if __name__=='__main__':
    app.run(debug=True)