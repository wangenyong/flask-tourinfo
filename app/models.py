from . import db
import jwt
import datetime
import time
from flask import current_app as app


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

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
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    watch_num = db.Column(db.Integer, default=0, nullable=False)
    star_num = db.Column(db.Integer, default=0, nullable=False)
    country = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    images = db.relationship('Image', backref='place')

    def to_json(self):
        json_place = {
            'name': self.name,
            'watch_num': self.watch_num,
            'star_num': self.star_num,
            'country': self.country,
            'city': self.city,
            'images': [image.to_json() for image in self.images]
        }
        return json_place


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey(
        'places.id'), nullable=False)

    def to_json(self):
        return self.url
