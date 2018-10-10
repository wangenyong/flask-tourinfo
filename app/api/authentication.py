import jwt
import datetime
import time
from . import api
from flask import jsonify, current_app as app, request
from .. import response as res
from ..models import User
from flask_httpauth import HTTPTokenAuth
from .errors import unauthorized


auth = HTTPTokenAuth(scheme='JWT')


@api.route('/login', methods=['POST'])
def login():
    openid = request.form['openid']
    session_key = request.form['session_key']

    token = User.encode_auth_token(openid, session_key)
    return jsonify(res.success('got token', {
        'token': token.decode()
    }))


@auth.verify_token
def verify_token(token):
    payload = User.decode_auth_token(token)
    if not isinstance(payload, str):
        openid = payload['data']['openid']
        if (openid is None):
            return False
        else:
            return True
    return False


@auth.error_handler
def auth_error():
    return unauthorized('Unauthorized access')
