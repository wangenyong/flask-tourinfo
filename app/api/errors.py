from flask import jsonify
from . import api
from .. import response as res


@api.app_errorhandler(403)
def forbidden(e):
    response = res.fail('forbidden')
    response.status_code = 403
    return response


@api.app_errorhandler(404)
def page_not_found(e):
    response = res.fail('not found', code=404)
    response.status_code = 404
    return response


@api.app_errorhandler(500)
def internal_server_error(e):
    response = res.fail('internal server error')
    response.status_code = 500
    return response
