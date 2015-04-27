#!/usr/bin/python
# -*- encoding: utf-8 -*-
from gerencianet.models import PaymentLog


def insert_log(notification, email=None):
    PaymentLog.objects.create(data=notification, email=email)