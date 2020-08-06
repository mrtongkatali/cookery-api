from db import db
from models.mixins import TimestampMixin
from flask_bcrypt import generate_password_hash, check_password_hash

class User(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60))
    status = db.Column(db.Integer, default="1")

    user_profile = db.relationship("UserProfile", backref="user", uselist=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(self, **kwargs):
        return self.query.filter_by(username=kwargs["username"]).first()

    @classmethod
    def find_by_id(self, id):
        return self.query.get(id)

    def __repr__(self):
        return '<User %r>' % self.username

class UserProfile(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photoFsRef = db.Column(db.Text())
    coverPhotoFsRef = db.Column(db.Text())
    tagline = db.Column(db.Text())
    short_bio = db.Column(db.Text(), nullable=False)
    country = db.Column(db.String(30))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user
