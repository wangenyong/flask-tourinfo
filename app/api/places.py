from flask import jsonify, request
from . import api
from ..models import Place, Image
from .. import db, photos, response as res
from .authentication import auth


@api.route('/place')
@auth.login_required
def get_place():
    places = Place.query.all()
    data = [place.to_json() for place in places]
    return jsonify(res.success('get place success', data))


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

