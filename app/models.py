from . import db
import jwt
import datetime
import time
from flask import current_app as app


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


watch = db.Table('watch',
                 db.Column('place_id', db.Integer, db.ForeignKey(
                     'place.id'), primary_key=True),
                 db.Column('user_id', db.Integer, db.ForeignKey(
                     'user.id'), primary_key=True)
                 )

star = db.Table('star',
                db.Column('place_id', db.Integer, db.ForeignKey(
                    'place.id'), primary_key=True),
                db.Column('user_id', db.Integer, db.ForeignKey(
                    'user.id'), primary_key=True)
                )


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    default = db.Column(db.Boolean, default=False, index=True, nullable=False)
    permissions = db.Column(db.Integer, nullable=False)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Follower': [Permission.FOLLOW],
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(64), unique=True, index=True, nullable=False)
    session_key = db.Column(db.String(255), unique=True, nullable=False)
    nick_name = db.Column(db.String(64))
    avatar_url = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    watch = db.relationship('Place', secondary=watch, lazy='dynamic',
                            backref=db.backref('watch_users', lazy='dynamic'))
    star = db.relationship('Place', secondary=star, lazy='dynamic',
                           backref=db.backref('star_users', lazy='dynamic'))
    traffic_infos = db.relationship('Traffic', backref='user', lazy='dynamic')
    hotel_infos = db.relationship('Hotel', backref='user', lazy='dynamic')
    food_infos = db.relationship('Food', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    @staticmethod
    def encode_auth_token(openid, session_key):
        """
        生成认证Token
        :param openid:
        :param session_key:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'morven',
                'data': {
                    'openid': openid,
                    'session_key': session_key
                }
            }
            return jwt.encode(
                payload,
                app.config["SECRET_KEY"],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, app.config["SECRET_KEY"], options={
                                 'verify_exp': False})
            if ('data' in payload and 'openid' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'


class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    country = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    images = db.relationship('Image', backref='place')
    traffic_infos = db.relationship('Traffic', backref='place', lazy='dynamic')
    hotel_infos = db.relationship('Hotel', backref='place', lazy='dynamic')
    food_infos = db.relationship('Food', backref='place', lazy='dynamic')

    def to_json(self):
        json_place = {
            'id': self.id,
            'name': self.name,
            'watch_num': self.watch_users.count(),
            'star_num': self.star_users.count(),
            'country': self.country,
            'city': self.city,
            'images': [image.to_json() for image in self.images]
        }
        return json_place


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey(
        'place.id'), nullable=False)

    def to_json(self):
        return self.url


class Traffic(db.Model):
    __tablename__ = 'traffic'
    __table_args__ = (
        db.UniqueConstraint('place_id', 'user_id', name='unique_place_user'),
    )
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    support_num = db.Column(db.Integer, nullable=False, default=0)
    place_id = db.Column(db.Integer, db.ForeignKey(
        'place.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def to_json(self):
        json_traffic = {
            'id': self.id,
            'content': self.content,
            'support_num': self.support_num
        }
        return json_traffic


class Hotel(db.Model):
    __tablename__ = 'hotel'
    __table_args__ = (
        db.UniqueConstraint('place_id', 'user_id', name='unique_place_user'),
    )
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    support_num = db.Column(db.Integer, nullable=False, default=0)
    place_id = db.Column(db.Integer, db.ForeignKey(
        'place.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def to_json(self):
        json_hotel = {
            'id': self.id,
            'content': self.content,
            'support_num': self.support_num
        }
        return json_hotel


class Food(db.Model):
    __tablename__ = 'food'
    __table_args__ = (
        db.UniqueConstraint('place_id', 'user_id', name='unique_place_user'),
    )
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    support_num = db.Column(db.Integer, nullable=False, default=0)
    place_id = db.Column(db.Integer, db.ForeignKey(
        'place.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def to_json(self):
        json_food = {
            'id': self.id,
            'content': self.content,
            'support_num': self.support_num
        }
        return json_food
