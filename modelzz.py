from db import db
from app import app
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from datetime import datetime

bcrypt = Bcrypt(app)

class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

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

    def __repr__(self):
        return '<User %r>' % self.username

class UserProfile(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photoFsRef = db.Column(db.String(50))
    short_bio = db.Column(db.Text(), nullable=False)
    country = db.Column(db.String(30))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user

class Dish(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(100))
    main_dish = db.Column(db.Integer)
    course = db.Column(db.Integer)
    cuisine = db.Column(db.Integer)
    prep_hour = db.Column(db.Integer, default="0")
    prep_minute = db.Column(db.Integer, default="0")
    cook_hour = db.Column(db.Integer, default="0")
    cook_minute = db.Column(db.Integer, default="0")
    serving_count = db.Column(db.Integer, default="1")
    status = db.Column(db.Integer, default="1")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instruction = db.relationship("PrepInstruction", backref="dish", uselist=True)
    ingredients = db.relationship("Ingredients", backref="dish", uselist=True)

    def __repr__(self):
        return '<Dish %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

class PrepInstruction(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    main_dish = db.Column(db.Integer)
    description = db.Column(db.Text())
    step_order = db.Column(db.Integer)

    def __repr__(self):
        return '<Instruction %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

class NutritionFacts(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    nutrition_label = db.Column(db.String(50))
    nutrition_value = db.Column(db.Float)

class Ingredients(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    amount = db.Column(db.String(20))
    unit = db.Column(db.String(20))
    ingredient_id = db.Column(db.Integer)
    ingredient_name = db.Column(db.String(200)) # for will be converted to just id after migration
    main_dish = db.Column(db.Integer) # for tracking, can be deleted after migration
    step_order = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()
