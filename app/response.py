from flask import jsonify


def success(msg, data='', code=200):
    return jsonify({
        'code': code,
        'msg': msg,
        'data': data
    })


def fail(msg, data='', code=-1):
    return jsonify({
        'code': code,
        'msg': msg,
        'data': data
    })
