# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class MonitorField(models.DateTimeField):
    description = _('Monitor fields')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', now)
        monitor = kwargs.pop('monitor', None)

        if not monitor:
            raise TypeError('{} requires a "monitor" argument'.format(self.__class__.__name__))

        self.monitor = monitor
        when = kwargs.pop('when', None)

        if when is not None:
            when = set(when)

        self.when = when
        super(MonitorField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.monitor_attname = '_monitor_{}'.format(name)
        models.signals.post_init.connect(self._save_initial, sender=cls)
        super(MonitorField, self).contribute_to_class(cls, name)

    def get_monitored_value(self, instance):
        return getattr(instance, self.monitor)

    def _save_initial(self, sender, instance, **kwargs):
        setattr(instance, self.monitor_attname, self.get_monitored_value(instance))

    def pre_save(self, model_instance, add):
        value = now()
        previous = getattr(model_instance, self.monitor_attname, None)
        current = self.get_monitored_value(model_instance)

        if previous != current:
            if self.when is None or current in self.when:
                setattr(model_instance, self.attname, value)
                self._save_initial(model_instance.__class__, model_instance)

        return super(MonitorField, self).pre_save(model_instance, add)

    def deconstruct(self):
        name, path, args, kwargs = super(MonitorField, self).deconstruct()
        kwargs['monitor'] = self.monitor

        if self.when is not None:
            kwargs['when'] = self.when

        return name, path, args, kwargs