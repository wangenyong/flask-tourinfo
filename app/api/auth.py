import jwt
import datetime
import time
from flask import jsonify, current_app as app
from .. import response as res


class Auth():
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
            payload = jwt.decode(auth_token, app.config["SECRET_KEY"], options={'verify_exp': False})
            if ('data' in payload and 'openid' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, openid, session_key):
        token = self.encode_auth_token(openid, session_key)
        return jsonify(res.success('got token', {
            'token': token.decode()
        }))

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
                result = res.fail('请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    openid = payload['data']['openid']
                    if (openid is None):
                        result = res.fail('找不到该用户信息')
                    else:
                        result = res.success('认证成功', openid)
                else:
                    result = res.fail(payload)
        else:
            result = res.fail('没有提供认证token')
        return result
