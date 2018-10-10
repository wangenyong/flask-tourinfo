from flask import jsonify, request
from . import api
from ..models import Place, Image
from .. import db, photos, response as res
from .auth import Auth


@api.route('/place')
def get_place():
    result = Auth.identify(Auth, request)
    if (result['code'] == 200):
        places = Place.query.all()
        data = [place.to_json() for place in places]
        result = res.success('get place success', data)
    return jsonify(result) 


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

        return jsonify(res.success('add place success')) 

