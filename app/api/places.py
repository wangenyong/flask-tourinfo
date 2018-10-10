from flask import jsonify, request, g
from . import api
from ..models import Place, Image, Permission
from .. import db, photos, response as res
from .authentication import auth
from ..decorators import permission_required


@api.route('/place')
@auth.login_required
@permission_required(Permission.WRITE)
def get_place():
    places = Place.query.all()
    if places is not None and len(places) > 0:
        data = [place.to_json() for place in places]
        return jsonify(res.success('get place success', data))
    return jsonify(res.fail('no data'))


@api.route('/place', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
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

