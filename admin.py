"""
Define all api
"""

import datetime
import json
import os.path as op
import random

from flask import (Flask, Response, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.contrib.mongoengine.filters import (BaseMongoEngineFilter,
                                                     BooleanEqualFilter)
from flask_admin.form import rules
from flask_admin.menu import MenuCategory, MenuLink, MenuView
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from client import *
from models import *


class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated

class NotAuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return not flask_login.current_user.is_authenticated

class UserView(ModelView): 
    column_filters = ['card_id'] 
    column_searchable_list = ('card_id',)
    # def is_accessible(self):
    #     return flask_login.current_user.is_authenticated
    def is_accessible(self):
        return flask_login.current_user.is_authenticated and flask_login.current_user.role == 'superadmin'

class ProtectView(ModelView):
    def is_accessible(self):
        return flask_login.current_user.is_authenticated and flask_login.current_user.role == 'superadmin'
