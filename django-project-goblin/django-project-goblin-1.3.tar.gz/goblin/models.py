if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.abspath(__file__)))

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

import re, math, logging
logger = logging.getLogger('goblin')

VERSION_REGEXP='\d(\.\d+)+(a|b|(\-(dev|test)))?'
    
class PublishStatus(models.Model):
    status = models.CharField(max_length=100)
    meaning = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return '%s'%self.status
    
class Publishable(models.Model):
    status = models.ForeignKey(PublishStatus)
    
    class Meta:
        abstract=True

class Version(list):

    RELEASE=0
    TEST=-1
    BETA=-2
    ALPHA=-3
    DEV=-4

    _STAGES = (RELEASE, DEV, ALPHA, BETA, TEST)
    _STAGES_STR = ('', '-dev', 'a', 'b', '-test')

    def __init__(self, *args):
        self.stage = Version.RELEASE
        if args[-1] in Version._STAGES:
            self.stage = args[-1]
            args = args[:-1] # simulating pop()
        for i in range(0, len(args)):
            if not isinstance(args[i], int):
                raise ValueError("Expected type of element %d to be"%i +
                                 " int. Got %s instead."%type(args[i]))
        super(Version, self).__init__(args)

    def _pad_either(self, other):
        # First, add the stage
        if len(self) < len(other):
            self.extend([0]*(len(other)-len(self)))
        elif len(self) > len(other):
            other.extend([0]*(len(self)-len(other)))
        return (self, other)

    def __eq__(self, other):
        (self, other) = self._pad_either(other)
        return super(Version, self).__eq__(other) or (
                super(Version, self).__eq__(other) and (self.stage ==
                                                  other.stage))


    def __lt__(self, other):
        (self, other) = self._pad_either(other)
        return super(Version, self).__lt__(other) or (
                super(Version, self).__eq__(other) and (self.stage < 
                                                        other.stage))


    def __gt__(self, other):
        (self, other) = self._pad_either(other)
        return super(Version, self).__gt__(other) or (
                super(Version, self).__eq__(other) and (self.stage >
                                                  other.stage))


    def __unicode__(self):
        s = '.'.join([str(i) for i in self])
        if self.stage:
            s += self._STAGES_STR[self.stage]
        return s

    def __str__(self):
        return unicode(self)

    def __repr__(self):
        return "<Version '%s'>"%unicode(self)

    @classmethod
    def from_str(Klass, string):
        if not re.match(r'%s'%VERSION_REGEXP, string):
            raise ValueError("'%s' is not the correct version format"%string)
        return Klass(*[int(i) for i in string.split('.')])

    def to_db(self):
        return '.'.join([str(i) for i in self]) + '.' + str(self.stage)

class VersionField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs.update({'max_length' : 30})
        super(VersionField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'varchar(500)'

    def to_python(self, value):
        if isinstance(value, Version):
            return value
        elif isinstance(value, str) or isinstance(value, unicode):
            return Version.from_str(value)
        logger.warn("%s could not be converted to %s"%(type(value),
                                                       type(self)))
        return None

    def get_prep_value(self, value):
        if not value:
            return "NULL"
        return value.to_db()
    
class ProjectManager(models.Manager):
    
    def with_statuses(self, statuses):
        from django.db import connection
        cursor = connection.cursor()
        query="""SELECT id
            from goblin_project
            WHERE status_id IN (
                SELECT id
                FROM goblin_publishstatus
                WHERE UPPER(status)
                IN (%s)
            )"""%(','.join(["'%s'"%s.upper() for s in statuses]))
        logger.debug("Executing %s"%query)
        cursor.execute(query)
        projects = []
        for row in cursor.fetchall():
            project = Project.objects.get(pk=row[0])
            projects.append(project)
        return projects

class Project(Publishable):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400,
        help_text=_("Short name for the project"))
    description = models.TextField()
    logo = models.ImageField(blank=True, null=True)
    README = models.TextField(blank=True, null=True,
                 help_text=_("reStructuedText supported"))
    homepage = models.URLField(blank=True, null=True)
    
    objects = ProjectManager()

    def __unicode__(self):
        releases = self.release_set.all()
        if len(releases) > 0:
            return "%s (%d releases)"%(self.name, len(releases))
        return "%s"%self.name

    def __str__(self):
        return unicode(self)
    
    def get_absolute_url(self):
        kwargs = {
            'project_slug' : self.slug,
        }
        return reverse('goblin.views.show_project', kwargs=kwargs,
            current_app='goblin')

    class Meta:
        verbose_name="Project"
        verbose_name_plural="Projects"
    
class ProjectLink(models.Model):
    type = models.CharField(max_length=100)
    url = models.URLField()
    project = models.ForeignKey('Project', related_name='project_links',
                                blank=True, null=True)
    release = models.ForeignKey('Release', related_name='project_links',
                                blank=True, null=True)

class NotLatestVersionException(ValidationError):

    def __init__(self, given, expected):
        """ Raised if a given version was expected to be greater than or
        equal to another version.

        :param given: Given version that was flagged.
        :type given: Version

        :param expected: Version that was expected to be the latest.
        """
        self.given = given
        self.expected = expected

    def __str__(self):
        return str("Expected a version higher than %s. "%self.expected +
            "Recieved %s"%self.given)

    def __repr__(self):
        return str("Expected a version higher than %s. "%self.expected +
            "Recieved %s"%self.given)

class Release(Publishable):
    
    project = models.ForeignKey(Project)
    version = VersionField()
    brief = models.TextField(help_text=_(mark_safe(
        "What features are part of this release? Note that changes can be" +
        " added with the <b>Changes</b> field.")))
    download = models.URLField(blank=True, null=True)
    release_logo = models.ImageField(blank=True, null=True,
        help_text=_("Leaving blank will use the project's logo."))

    release_date = models.DateField(auto_now=True,
       help_text=_("When was this version released?"))

    def __unicode__(self):
        return "%s %s"%(self.project, self.version)

    def save(self, *args, **kwargs):
        self.clean()
        return super(Release, self).save(*args, **kwargs)

    def clean(self):
        logger.debug("Cleaning a release.")
        latest = None
        if self.project:
            logger.debug("Finding latest version...")
            for r in self.project.release_set.all():
                """ NOTE that r.version is not a VersionField as expected.
                This is due to the Python error
                https://code.djangoproject.com/ticket/14518
                """
                latest = Version.from_str(r.version)
            logger.debug("Latest version is %s."%latest)
            if latest and (self.version < latest):
                raise NotLatestVersionException(self.version, latest)
                
    def get_absolute_url(self):
        kwargs = {
            'project_slug' : self.project.slug,
            'version' : str(self.version),
        }
        return reverse(goblin.views.project_release, kwargs=kwargs,
            current_app='goblin')

    class Meta:
        verbose_name='Release'
        verbose_name_plural='Releases'

class Change(Publishable):
    ACTIONS = (
        ('+', "Add"),
        ('-', "Remove"),
        ('*', "Fix"),
        ('>', "Other"),
    )
    release = models.ForeignKey(Release)
    action = models.CharField(choices=ACTIONS, max_length=3)
    what = models.TextField()

    class Meta:
        verbose_name='Change'
        verbose_name_plural='Changes'
        app_label='goblin'

