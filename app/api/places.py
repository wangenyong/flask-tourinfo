from flask import jsonify
from flask import request
from . import api
from .. import db
from ..models import Place, Image
from .. import photos


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
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        name = request.form['name']
        country = request.form['country']
        city = request.form['city']
        url = photos.url(filename)

        img = Image(url=url)
        place = Place(name=name, country=country, city=city)
        place.images = [img]
        db.session.add(place)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'code': 10000,
            'message': "add place success"
        })
