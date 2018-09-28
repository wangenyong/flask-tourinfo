from flask import jsonify
from . import api

@api.route('/place')
def get_place():
    return jsonify({
        'place': 'Hello place',
    })