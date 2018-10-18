from flask import jsonify, request, g, current_app as app
from . import api
from ..models import Place, Image, Permission, Traffic, Hotel, Food
from .. import db, photos, response as res
from .authentication import auth
from ..decorators import permission_required
from sqlalchemy import exc


@api.route('/place')
@auth.login_required
@permission_required(Permission.WRITE)
def get_all_place():
    places = Place.query.all()
    if places is not None and len(places) > 0:
        data = [place.to_json() for place in places]
        return jsonify(res.success('get place success', data))
    return jsonify(res.fail('no data'))


@api.route('/place', methods=['POST'])
@auth.login_required
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


@api.route('/place/<int:id>/status')
@auth.login_required
def get_status(id):
    place = Place.query.filter_by(id=id).first()
    user = g.current_user
    watched = place.watch_users.filter_by(id=user.id).first() is not None
    stared = place.star_users.filter_by(id=user.id).first() is not None
    data = {
        'watched': watched,
        'stared': stared
    }
    return jsonify(res.success('get status success', data))


@api.route('/place/<int:id>/star', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def star(id):
    place = Place.query.filter_by(id=id).first()
    user = g.current_user
    exists = place.star_users.filter_by(id=user.id).first() is not None
    if exists:
        place.star_users.remove(user)
        message = 'cancel star success'
        stared = False
    else:
        place.star_users.append(user)
        message = 'star success'
        stared = True
    db.session.commit()
    return jsonify(res.success(message, {
        'stared': stared
    }))


@api.route('/place/<int:id>/watch', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def watch(id):
    place = Place.query.filter_by(id=id).first()
    user = g.current_user
    exists = place.watch_users.filter_by(id=user.id).first() is not None
    if exists:
        place.watch_users.remove(user)
        message = 'cancel watch success'
        watched = False
    else:
        place.watch_users.append(user)
        message = 'watch success'
        watched = True
    db.session.commit()
    return jsonify(res.success(message, {
        'watched': watched
    }))


@api.route('/place/<int:id>/traffic')
@auth.login_required
def get_traffic(id):
    traffics = Traffic.query.filter_by(place_id=id).all()
    if traffics is not None and len(traffics) > 0:
        data = [traffic.to_json() for traffic in traffics]
        return jsonify(res.success('get traffic success', data))
    return jsonify(res.fail('no data'))


@api.route('/place/<int:id>/traffic', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def add_traffic(id):
    place = Place.query.filter_by(id=id).first()
    user = g.current_user
    content = request.form['content']
    traffic = Traffic(content=content)
    traffic.place = place
    traffic.user = user
    try:
        db.session.add(traffic)
        db.session.commit()
    except exc.IntegrityError:
        return jsonify(res.fail('You have add traffic!'))
    return jsonify(res.success('add traffic success'))


@api.route('/place/traffic/<int:id>/evaluate', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def traffic_evaluate(id):
    step = request.form['step']
    user = g.current_user
    traffic = Traffic.query.filter_by(id=id).first()
    exists = traffic.evaluate_users.filter_by(id=user.id).first() is not None
    if exists:
        return jsonify(res.fail('You have evaluated!'))
    traffic.support_num += int(step)
    traffic.evaluate_users.append(user)
    db.session.commit()
    return jsonify(res.success('evaluate traffic success'))


@api.route('/place/<int:id>/hotel')
@auth.login_required
def get_hotel(id):
    hotels = Hotel.query.filter_by(place_id=id).all()
    if hotels is not None and len(hotels) > 0:
        data = [hotel.to_json() for hotel in hotels]
        return jsonify(res.success('get hotel success', data))
    return jsonify(res.fail('no data'))


@api.route('/place/<int:id>/hotel', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def add_hotel(id):
    place = Place.query.filter_by(id=id).first()
    user = g.current_user
    content = request.form['content']
    hotel = Hotel(content=content)
    hotel.place = place
    hotel.user = user
    try:
        db.session.add(hotel)
        db.session.commit()
    except exc.IntegrityError:
        return jsonify(res.fail('You have add hotel!'))
    return jsonify(res.success('add hotel success'))


@api.route('/place/hotel/<int:id>/evaluate', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def hotel_evaluate(id):
    step = request.form['step']
    user = g.current_user
    hotel = Hotel.query.filter_by(id=id).first()
    exists = hotel.evaluate_users.filter_by(id=user.id).first() is not None
    if exists:
        return jsonify(res.fail('You have evaluated!'))
    hotel.support_num += int(step)
    hotel.evaluate_users.append(user)
    db.session.commit()
    return jsonify(res.success('evaluate hotel success'))


@api.route('/place/<int:id>/food')
@auth.login_required
def get_food(id):
    foods = Food.query.filter_by(place_id=id).all()
    if foods is not None and len(foods) > 0:
        data = [food.to_json() for food in foods]
        return jsonify(res.success('get food success', data))
    return jsonify(res.fail('no data'))


@api.route('/place/<int:id>/food', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def add_food(id):
    place = Place.query.filter_by(id=id).first()
    user = g.current_user
    content = request.form['content']
    food = Food(content=content)
    food.place = place
    food.user = user
    try:
        db.session.add(food)
        db.session.commit()
    except exc.IntegrityError:
        return jsonify(res.fail('You have add food!'))
    return jsonify(res.success('add food success'))


@api.route('/place/food/<int:id>/evaluate', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def food_evaluate(id):
    step = request.form['step']
    user = g.current_user
    food = Food.query.filter_by(id=id).first()
    exists = food.evaluate_users.filter_by(id=user.id).first() is not None
    if exists:
        return jsonify(res.fail('You have evaluated!'))
    food.support_num += int(step)
    food.evaluate_users.append(user)
    db.session.commit()
    return jsonify(res.success('evaluate food success'))
