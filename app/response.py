
def success(msg, data='', code=200):
    return {
        'code': code,
        'msg': msg,
        'data': data
    }


def fail(msg, data='', code=-1):
    return {
        'code': code,
        'msg': msg,
        'data': data
    }
