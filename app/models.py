from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    watch_num = db.Column(db.Integer, default=0, nullable=False)
    star_num = db.Column(db.Integer, default=0, nullable=False)
    country = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    images = db.relationship('Image', backref='place')

    def to_json(self):
        json_place = {
            'name': self.name,
            'watch_num': self.watch_num,
            'star_num': self.star_num,
            'country': self.country,
            'city': self.city,
            'images': [image.to_json() for image in self.images]
        }
        return json_place


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)

    def to_json(self):
        return self.url
