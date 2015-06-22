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

# User Struct.
UserStruct = portfolio.component.model.user_struct(db)

# Post Struct
PostStruct = portfolio.component.model.post_struct(db, UserStruct)

# A simple Note table
class MyNote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(UserStruct.User.id))
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    user = db.relationship(UserStruct.User, backref="notes")


