"""
Portfolio

model.py

You may place your models here.
"""

from active_alchemy import SQLAlchemy
import portfolio.component.model
from . import get_config

config = get_config()

db = SQLAlchemy(config.DATABASE_URI)

# User Model
UserModel = portfolio.component.model.user_model(db)

# Post Model
PostModel = portfolio.component.model.post_model(UserModel)

# A simple Note table
class MyNote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.User.id))
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    user = db.relationship(UserModel.User, backref="notes")
