# coding: utf-8

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Manager(BaseUserManager):
    def create_user(self, username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.experience = User.BEGINNER
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.experience = User.EXPERT
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    experience: Level of experience, how complicated edit surface will the author have.
    """
    BEGINNER = 1
    INTERMEDIATE = 2
    EXPERT = 3

    EXPERIENCE_CHOICES = (
        (BEGINNER, _('beginner')),
        (INTERMEDIATE, _('intermediate')),
        (EXPERT, _('expert')),
    )
    username = models.CharField(max_length=50, unique=True)
    experience = models.SmallIntegerField(_('experience'), max_length=10, choices=EXPERIENCE_CHOICES)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    nickname = models.CharField(_('nickname'), max_length=20, blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into bangoo admin site'))
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = Manager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.nickname or self.username
