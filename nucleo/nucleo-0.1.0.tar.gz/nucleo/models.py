from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


# Post model
class Post(models.Model):
    date = models.DateTimeField(default=datetime.now)
    text = models.CharField(max_length=250)
    author = models.ForeignKey(User)


#  UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    follows = models.ManyToManyField('self', related_name='followed_by',
                                     symmetrical=False)

    def __unicode__(self):
        return self.user.username
