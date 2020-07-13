from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

"""
DESIGN DOC

General Overview

PHASE 1:
- Create a web application for sharing homemade cooked meals.
- As a user, I can create an account to the site, then make my own recipe.
- As a user, I can publish my own recipe or make it private
- As a user, my recipe can be peer reviewed and rated by other users
- As a user, I can review or bookmark someone's public recipe
- As a user, I can search a recipe using my available ingredients

PHASE 2:
- As as user, I

"""
