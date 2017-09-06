"""
Define all api
"""

import datetime
import json
import os.path as op
import random

from flask import abort, Flask, jsonify, redirect, render_template, request, url_for
from flask_admin import Admin

from flask_babelex import Babel
from flask_admin.contrib.mongoengine import ModelView
# from flask.ext.babelex import Babel
import admin as am
from client import *
from models import User, Member, Club, DepositRecord, Property, PropertyCategory, Role
import flask_login
# app.config.from_pyfile('config.py')
from flask import Flask
from werkzeug.contrib.cache import MemcachedCache, SimpleCache
from flask_mongoengine import MongoEngine


app = Flask("UHE", instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)
db = MongoEngine(app)


CACHE = SimpleCache()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(card_id):
    return User.objects(card_id=card_id).first()


babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
ProtectView = am.ProtectView
admin = Admin(app, name='上海大学社团管理', template_mode='bootstrap3')
admin.add_view(ProtectView(User, name='用户管理'))
admin.add_view(ProtectView(Member, name='成员管理',))
admin.add_view(ProtectView(Club, name='社团管理'))
admin.add_view(ProtectView(DepositRecord, name='经费流水'))
admin.add_view(ProtectView(Property, name='资产管理'))
admin.add_view(ProtectView(PropertyCategory, name='资产分类'))
admin.add_view(ProtectView(Role, name='角色管理'))
admin.add_link(am.NotAuthenticatedMenuLink(name='登录',
                                           endpoint='login_view'))
admin.add_link(am.AuthenticatedMenuLink(name='注销',
                                        endpoint='logout_view'))


def validate(card_id, password):
    client = Services()
    client.card_id = card_id
    client.password = password
    if client.login() and client.get_data():
        result = {
            'success': True,
            'name': client.data['name'],
            'card_id': card_id
        }
    else:
        result = {
            'success': False
        }
    return result


@app.route('/')
def index():
    return redirect('/admin')


@app.route('/reg/osc', methods=['GET', 'POST'])
def reg_osc():
    if request.method == 'POST':
        data = request.get_json()
        card_id = data['card_id']
        password = data['password']
        user = User.objects(card_id=card_id).first()
        result = validate(card_id, password)
        phone = data['phone']
        email = data['email']
        club = Club.objects(name='开源社区').first()
        if result['success']:
            if user is None:
                user = User(name=result['name'],
                            card_id=card_id, role='student', phone=phone, email=email)
                user.save()
            if club not in user.clubs:
                user.clubs.append(club)
                user.save()
                Member(club=club, member=user).save()
        else:
            abort(401)
        return jsonify(status='ok')
    else:
        return render_template('reg.html')


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        card_id = request.form['card_id']
        password = request.form['password']
        user = User.objects(card_id=card_id).first()
        result = validate(card_id, password)
        if result['success']:
            if user is None:
                user = User(name=result['name'],
                            card_id=card_id, role='student')
                user.save()
            flask_login.login_user(user)
        else:
            user = User()
        return redirect('/admin')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout_view():
    flask_login.logout_user()
    return redirect(url_for('admin.index'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5001)
