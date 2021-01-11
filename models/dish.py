import logging

from db import db
from models.mixins import TimestampMixin
from models.ingredient import Ingredients
from models.prep_instruction import PrepInstruction
from models.user import User

from sqlalchemy.sql import text
from sqlalchemy.orm import joinedload, subqueryload, contains_eager, aliased, selectinload
from sqlalchemy import and_, or_, not_

logger = logging.getLogger("app.access")

class Dish(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(100))
    main_dish = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=True)
    course = db.Column(db.Integer)
    cuisine = db.Column(db.Integer)
    prep_hour = db.Column(db.Integer, default="0")
    prep_minute = db.Column(db.Integer, default="0")
    cook_hour = db.Column(db.Integer, default="0")
    cook_minute = db.Column(db.Integer, default="0")
    serving_count = db.Column(db.Integer, default="1")
    es_keywords = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, default="1")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # user = db.relationship(User)
    instruction = db.relationship(PrepInstruction, backref="dish")
    ingredients = db.relationship(Ingredients, backref="dish")

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
    def get_dish_import(self, **kwargs):
        try:
            query = (
                db.session.query(Dish)
                .paginate(int(kwargs["page"]), int(kwargs["size"]), error_out=False)
            )

            return query
        except Exception as e:
            logging.debug(f"[err] Dish.get_dish_import :: {kwargs} => {e}")

    @classmethod
    def get_all_dishes(self, **kwargs):
        sort = kwargs["sort"] if "sort" in kwargs else "dish.id desc"
        # sort = "id asc"
        # .order_by(self.id.desc()) \

        try:
            fields = ['id', 'dish_name', 'main_dish', 'description', 'course', 'cuisine', 'prep_hour', 'prep_minute', 'cook_hour', 'cook_minute', 'serving_count', 'status']
            entities = [getattr(Dish, field) for field in fields]

            query = (
                db.session.query()
                .with_entities(*entities)
                .order_by(text(sort))
                .paginate(int(kwargs["page"]), int(kwargs["size"]), error_out=False)
            )

            return query
        except Exception as e:
            logging.debug(f"[err] Dish.get_all_dishes :: {kwargs} => {e}")

    @classmethod
    def find_by_id(self, dish_id):
        try:
            query = (
                db.session.query(Dish)
                .options(contains_eager(Dish.ingredients))
                .outerjoin(Ingredients, and_(Dish.id == Ingredients.dish_id, Ingredients.status == 1))
                .options(contains_eager(Dish.instruction))
                .outerjoin(PrepInstruction, and_(Dish.id == PrepInstruction.dish_id, PrepInstruction.status == 1))
                .filter(Dish.id == dish_id)
                .order_by(Ingredients.step_order.asc())
                .order_by(PrepInstruction.step_order.asc())
                .scalar()
            )

            return query
        except Exception as e:
            logging.debug(f"[err] Dish.find_by_id({dish_id}) => {e}")

class NutritionFacts(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    nutrition_label = db.Column(db.String(50))
    nutrition_value = db.Column(db.Float)
