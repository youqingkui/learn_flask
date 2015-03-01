#!/usr/bin/env python
# coding=utf-8

from flask import Flask, render_template, request
from flask.ext.script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    comments = [1,2,3,4,5,6]
    return render_template('index.html', comments = comments)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name = name)



if __name__ == '__main__':
    manager.run()