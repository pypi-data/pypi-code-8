import subprocess
import os
import saddle
import shutil
import subprocess
import sys
import contextlib

# TODO : Python service with lines of code covered, etc.
# TODO : Django fixtures + django settings fixtures

class DjangoService(saddle.Service):
    def __init__(self, service_engine, port=18080, python=sys.executable, settings=None, needs=None, fixtures=[]):
        self.port = port
        self.python = python
        self.django_fixtures = fixtures
        self.settings = settings
        self.settings_option = [] if settings is None else ['--settings=' + settings, ]
        command = [python, "-u", service_engine.directory + os.sep + 'manage.py', 'runserver', str(port), '--noreload', ] + self.settings_option
        super(DjangoService, self).__init__(
            service_engine,
            "Django", command,
            {'logline': lambda line: "Quit the server with CONTROL-C." in line,},
            needs=needs,
            directory=service_engine.directory
        )

    def setup(self):
        #sys.stdout.write("Syncing database...\n")
        #self.manage("syncdb", "--noinput")
        sys.stdout.write("Running migrations...\n")
        self.manage("migrate")
        sys.stdout.write("Updating site...\n")
        with self.context_models() as models:
            if 'django.contrib.sites.models.Site' in models:
                Site = models['django.contrib.sites.models.Site']
                site = Site.objects.all()[0]
                site.domain = "localhost:{}".format(self.port)
                site.name = "localhost:{}".format(self.port)
                site.save()
        for fixture in self.django_fixtures:
            print "manage.py loaddata {}".format(fixture)
            self.manage("loaddata", fixture)

    def manage(self, *args):
        """Run manage command."""
        os.chdir(self.directory)
        self.run([self.python, "-u", self.directory + os.sep + 'manage.py', ] + list(args) + self.settings_option)

    def url(self):
        """Return a URL for the Django site."""
        return "localhost:{}".format(self.port)

    def savefixture(self, filename):
        """Saves a JSON database fixture."""
        self.manage("dumpdata", filename)

    @contextlib.contextmanager
    def context_models(self):
        import django
        if django.VERSION[:2] < (1, 7):
            raise RuntimeError("Cannot import models for versions of django below 1.7")
        elif django.VERSION[:2] >= (1, 7):
            os.chdir(self.directory)
            old_django_settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "")
            os.environ['DJANGO_SETTINGS_MODULE'] = '' if self.settings is None else self.settings
            django.setup()
            yield {x.__module__ + '.' + x.__name__:x for x in django.apps.apps.get_models()}
            os.environ['DJANGO_SETTINGS_MODULE'] = old_django_settings_module
