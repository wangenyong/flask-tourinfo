from flask import jsonify
from . import api
from .. import response as res


@api.app_errorhandler(403)
def forbidden(e):
    response = jsonify(res.fail('forbidden')) 
    response.status_code = 403
    return response


@api.app_errorhandler(404)
def page_not_found(e):
    response = jsonify(res.fail('not found', code=404)) 
    response.status_code = 404
    return response


@api.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify(res.fail('internal server error')) 
    response.status_code = 500
    return response
