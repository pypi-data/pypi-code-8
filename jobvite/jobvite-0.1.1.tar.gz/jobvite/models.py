from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def to_dict(self):
        return dict([(f, getattr(self, f))
                        for f in ('name', 'slug', 'description')])

class Position(models.Model):
    job_id = models.CharField(max_length=25)
    title = models.CharField(max_length=100)
    requisition_id = models.CharField(max_length=20)
    category = models.ForeignKey(Category, null=True, blank=True)
    job_type = models.CharField(max_length=255)
    location = models.CharField(max_length=150, null=True, blank=True)
    date = models.CharField(max_length=100)
    detail_url = models.URLField()
    apply_url = models.URLField()
    description = models.TextField()
    brief_description = models.TextField(null=True, blank=True)
    location_filter = models.CharField(max_length=255, blank=True, default='')

    def __unicode__(self):
        return u"%s - %s" % (self.job_id, self.title)

    def get_absolute_url(self):
        return ('jobvite-position', (), {
            'job_id': self.job_id,
        })

    def to_dict(self):
        d = dict([(f, getattr(self, f))
                    for f in (
                        'job_id', 'title', 'requisition_id',
                        'job_type', 'location', 'date', 'detail_url',
                        'apply_url', 'description', 'brief_description',
                        'location_filter'
                    )])

        d.update({
            'category': self.category.to_dict() if self.category else None
        })

        return d
