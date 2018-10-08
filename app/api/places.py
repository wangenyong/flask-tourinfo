from flask import jsonify
from flask import request
from . import api
from .. import db
from ..models import Place

@api.route('/place')
def get_place():
    res = Place.query.all()
    return jsonify({
        'status': 'success',
        'code': 10000,
        'message': 'get place success',
        'data': [place.to_json() for place in res]
    })

@api.route('/place', methods=['POST'])
def add_place():
    name = request.form['name']
    place = Place(name=name)
    db.session.add(place)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'code': 10000,
        'message': "add place success"
    })