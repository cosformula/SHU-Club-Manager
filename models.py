import datetime

import flask_login
from flask_mongoengine import MongoEngine
from mongoengine import (BooleanField, DateTimeField, Document, EmailField,
                         EmbeddedDocument, EmbeddedDocumentField, FloatField,
                         ImageField, IntField, ListField, ReferenceField,
                         StringField, connect, queryset_manager, signals)


class Club(Document):
    name = StringField()
    desc = StringField()
    create = DateTimeField(default=datetime.datetime.now)
    meta = {
        'strict': False
    }

    def __unicode__(self):
        return self.name


class User(flask_login.UserMixin, Document):
    email = EmailField()
    name = StringField()
    nickname = StringField()
    card_id = StringField(primary_key=True)
    phone = StringField()
    role = StringField()
    create_time = DateTimeField(default=datetime.datetime.now)
    clubs = ListField(ReferenceField(Club),default=[])
    meta= {
        'strict': False
    }

    def __unicode__(self):
        return self.card_id + self.name

    def get_id(self):
        return self.card_id


class Role(Document):
    club = ReferenceField(Club)
    name = StringField()
    meta = {
        'strict': False
    }

    def __unicode__(self):
        return self.name


class PropertyCategory(Document):
    club = ReferenceField(Club)
    name = StringField()
    meta = {
        'strict': False
    }

    def __unicode__(self):
        return self.name


class Member(Document):
    club = ReferenceField(Club)
    member = ReferenceField(User)
    roles = ListField(ReferenceField(Role))
    remark = StringField()
    come_from = StringField()
    core = BooleanField(default=False)
    activate = BooleanField(default=False)
    leave = BooleanField(default=False)
    meta = {
        'strict': False
    }

    def __unicode__(self):
        return str(self.member)


class Log(EmbeddedDocument):
    time = DateTimeField(default=datetime.datetime.now)
    content = StringField()
    operator = ReferenceField(Member)
    meta = {
        'strict': False
    }

    def __unicode__(self):
        return self.content


class DepositRecord(Document):
    club = ReferenceField(Club)
    value = FloatField()
    handler = ReferenceField(Member)
    remark = StringField()
    meta = {
        'strict': False
    }


class Property(Document):
    club = ReferenceField(Club)
    name = StringField()
    source = StringField()
    handler = ReferenceField(Member)
    created = DateTimeField(default=datetime.datetime.now)
    quantity = IntField(default=1)
    origin_value = FloatField()
    current_value = FloatField()
    category = ReferenceField(PropertyCategory)
    place = StringField()
    created = DateTimeField(default=datetime.datetime.now)
    last_modify = DateTimeField(default=datetime.datetime.now)
    operation_log = ListField(EmbeddedDocumentField(Log))
    delete_time = DateTimeField()
    deleted = BooleanField()
    remark = StringField()
    meta = {
        'strict': False
    }

    def __unicode__(self):
        return self.name
