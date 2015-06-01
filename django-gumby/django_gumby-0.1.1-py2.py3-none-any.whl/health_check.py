from datetime import datetime, timedelta
from time import sleep

from django.db import DatabaseError, IntegrityError
from django.core.cache.backends.base import CacheKeyWarning
from django.core.cache import cache
from django.conf import settings

from gumby.basehealthcheck import BaseHealthCheck
from gumby.models import HealthCheckModel
from gumby.healthchecks import healthchecks_dir
from gumby.tasks import add


class DjangoDatabaseBackend(BaseHealthCheck):

    def check_status(self):
        try:
            obj = HealthCheckModel.objects.create(title="test")
            obj.title = "newtest"
            obj.save()
            obj.delete()
            self.status = True
        except IntegrityError:
            self.status = False
            self.extras["response"] = "integrety error"
        except DatabaseError:
            self.status = False
            self.extras["response"] = "integrety error"


class CacheBackend(BaseHealthCheck):

    def check_status(self):
        try:
            cache.set('djangohealtcheck_test', 'itworks', 1)
            if cache.get("djangohealtcheck_test") == "itworks":
                self.status = True
            else:
                self.status = False
                self.extras["response"] = "Cache key does not match"
        except CacheKeyWarning:
            self.status = False
            self.extras["response"] = "Cache key warning"
        except ValueError:
            self.status = False
            self.extras["response"] = "ValueError"
        except Exception:
            self.status = False
            self.extras["response"] = "Unknown exception"


class CeleryHealthCheck(BaseHealthCheck):

    def check_status(self):
        timeout = getattr(settings, 'HEALTHCHECK_CELERY_TIMEOUT', 3)

        try:
            result = add.apply_async(args=[4, 4], expires=datetime.now() + timedelta(seconds=timeout))
            now = datetime.now()
            while (now + timedelta(seconds=3)) > datetime.now():
                #print "            checking...."
                if result.ready():
                    result.forget()
                    self.status = True
                    return True
                sleep(0.1)
        except IOError:
            pass
        self.status = False
        self.extras["response"] = "Unknown error"

healthchecks_dir.register(DjangoDatabaseBackend)
healthchecks_dir.register(CacheBackend)
healthchecks_dir.register(CeleryHealthCheck)
