#!/usr/bin/env python
# coding=utf-8

from flask import Flask, render_template, request,\
    session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from datetime import datetime

app = Flask(__name__)



manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'hard to guess string'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods = ['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            print "hi"
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            print "to"
            session['known'] = True

        session['name'] = form.name.data
        return redirect(url_for('index'))


    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name = name)



def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()