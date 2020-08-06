from db import db
from models.mixins import TimestampMixin

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

    @classmethod
    def get_all_dishes(self, **kwargs):
        return self.query \
            .order_by(self.id.desc()) \
            .paginate(int(kwargs["page"]), int(kwargs["size"]), error_out=False)

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
