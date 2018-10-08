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
    star_num = db.Column(db.Integer, default=0, nullable=False)
    like_num = db.Column(db.Integer, default=0, nullable=False)

    def to_json(self):
        json_place = {
            'name': self.name,
            'star_num': self.star_num,
            'like_num': self.like_num
        }
        return json_place
