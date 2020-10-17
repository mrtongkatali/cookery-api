from db import db
from models.mixins import TimestampMixin
from models.ingredient import Ingredients
from models.prep_instruction import PrepInstruction

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
    instruction = db.relationship(PrepInstruction, backref="dish", uselist=True)
    ingredients = db.relationship(Ingredients, backref="dish", uselist=True)

    def __repr__(self):
        return '<Dish %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
          setattr(self, key, item)

        db.session.commit()

    @classmethod
    def get_all_dishes(self, **kwargs):
        from sqlalchemy.sql import text

        sort = kwargs["sort"] if "sort" in kwargs else "id desc"
        # sort = "id asc"
        # .order_by(self.id.desc()) \
        return self.query \
            .order_by(text(sort)) \
            .paginate(int(kwargs["page"]), int(kwargs["size"]), error_out=False)

    @classmethod
    def find_by_id(self, dish_id):
        return self.query.get(dish_id)

class NutritionFacts(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    nutrition_label = db.Column(db.String(50))
    nutrition_value = db.Column(db.Float)
