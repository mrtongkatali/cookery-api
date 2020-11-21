from db import db
from models.mixins import TimestampMixin

class Ingredients(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    amount = db.Column(db.Float(5))
    unit = db.Column(db.String(20))
    grocery_item_id = db.Column(db.Integer)
    ingredient_name = db.Column(db.String(200)) # for will be converted to just id after migration
    additional_note = db.Column(db.Text(), nullable=True)
    main_dish = db.Column(db.Integer) # for tracking, can be deleted after migration
    step_order = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
          setattr(self, key, item)

        db.session.commit()

    @classmethod
    def find_by_id(self, ingr_id):
        return self.query.get(ingr_id)
