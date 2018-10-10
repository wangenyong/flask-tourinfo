from flask import jsonify
from . import api


@api.app_errorhandler(403)
def forbidden(e):
    response = jsonify({
        'status': 'fail',
        'code': 404,
        'message': 'forbidden',
    })
    response.status_code = 403
    return response


@api.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({
        'status': 'fail',
        'code': 404,
        'message': 'not found',
    })
    response.status_code = 404
    return response


@api.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({
        'status': 'fail',
        'code': 500,
        'message': 'internal server error',
    })
    response.status_code = 500
    return response
