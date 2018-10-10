from flask import request
from . import api
from .auth import Auth

@api.route('/login', methods=['POST'])
def login():
    openid = request.form['openid']
    session_key = request.form['session_key']
    
    return Auth.authenticate(Auth, openid, session_key)



