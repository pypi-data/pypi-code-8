"""
Portfolio

model.py

You may place your models here.
"""

from active_alchemy import SQLAlchemy
from . import get_config
from portfolio.component import user_account, cms_post


config = get_config()

db = SQLAlchemy(config.DATABASE_URI)

# User Model
UserModel = user_account.model(db)

# Post Model
CmsPostModel = cms_post.model(UserModel)

# A simple Note table
class MyNote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.User.id))
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    user = db.relationship(UserModel.User, backref="notes")
