import logging

from db import db
from models.mixins import TimestampMixin

class PrepInstruction(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    main_dish = db.Column(db.Integer)
    description = db.Column(db.Text())
    step_order = db.Column(db.Integer)
    status = db.Column(db.Integer, default="1")

    def __repr__(self):
        return '<Instruction %r>' % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
          setattr(self, key, item)

        db.session.commit()

    @classmethod
    def find_by_id(self, id):
        try:
            return self.query.get(id)
        except Exception as e:
            logging.debug(f"[err] PrepInstruction.find_by_id({id}) => {e}")
            return None

    @classmethod
    def find_last_step(self, dish_id):
        try:
            query = (
                db.session.query()
                .with_entities('step_order')
                .filter(PrepInstruction.dish_id == dish_id)
                .order_by(PrepInstruction.step_order.desc())
                .first()
            )

            return query
        except Exception as e:
            logging.debug(f"[err] PrepInstruction.find_last_step({dish_id}) => {e}")
            return None
