import jwt
import datetime
import time
from flask import jsonify, current_app as app
from .. import response as res


class Auth():
    @staticmethod
    def encode_auth_token(openid, session_key):
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

    def authenticate(self, openid, session_key):
        token = self.encode_auth_token(openid, session_key)
        return res.success('got token', {
            'token': token.decode()
        })
