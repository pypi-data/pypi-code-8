import json
import datetime
import random
from logging import Handler

from django.utils import timezone


class DBHandler(Handler, object):

    model_name = None
    expiry = None

    def __init__(self, model="", expiry=0):
        super(DBHandler, self).__init__()
        self.model_name = model
        self.expiry = int(expiry)

    def emit(self, record):
        try:
            try:
                model = self.get_model(self.model_name)
            except Exception:
                from .models import GeneralLog as model

            log_entry = model(level=record.levelname, message=self.format(record))

            try:
                data = json.loads(record.msg)
                for key, value in data.items():
                    if hasattr(log_entry, key):
                        setattr(log_entry, key, value)
            except Exception:
                pass
            log_entry.save()

            if self.expiry and random.randint(1, 5) == 1:
                model.objects.filter(time__lt=timezone.now() - datetime.timedelta(seconds=self.expiry)).delete()
        except Exception:
            pass

    def get_model(self, name):
        names = name.split('.')
        mod = __import__('.'.join(names[:-1]), fromlist=names[-1:])
        return getattr(mod, names[-1])
