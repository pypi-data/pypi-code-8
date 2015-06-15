import os
from datetime import date

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from mezzanine.core.fields import FileField
from mezzanine_sermons.validators import validate_mp3_extension


class SermonSeries(models.Model):
    """
    A model to describe a sermon series
    """
    title = models.CharField(max_length=60,
                             help_text="The name of the sermon series")
    bible_passage = models.CharField(max_length=100,
                                     help_text="The bible passage for the sermon series",
                                     blank=True)
    description = models.TextField()
    start_date = models.DateField(blank=False,
                                  help_text="This helps us order the sermon series")
    image = FileField(verbose_name="Image", max_length=255, blank=True,
                      help_text="Use the media manager to upload and select an image for the sermon series")

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Sermon Series"
        verbose_name_plural = "Sermon Series"

    def __str__(self):
        title1 = self.title
        title2 = ""
        if self.bible_passage != "":
            title2 = " (" + self.bible_passage + ")"
        title = title1 + title2
        return title


class Sermon(models.Model):
    series = models.ForeignKey(SermonSeries, blank=True, null=True)
    title = models.CharField(max_length=60)
    passage = models.CharField(max_length=100, help_text="The bible passage for the individual sermon",
                               blank=True)
    preacher = models.CharField(max_length=100, blank=True)
    date = models.DateField(blank=False)
    audio = FileField(verbose_name="The audio file", max_length=255, blank=True,
                      help_text="Select the audio file using the file manager (Only .mp3 files accepted)")

    class Meta:
        ordering = ['-date']
        verbose_name = "Individual Sermon"
        verbose_name_plural = "Individual Sermons"

    def __str__(self):
        title1, title2, title3, title4, titleseries = self.title, "", "", "", ""
        if self.passage != "":
            title2 = " (" + self.passage + ")"
        if self.series:
            titleseries = " in series '" + self.series.title + "',"
        if self.preacher != "":
            title3 = " by " + self.preacher
        if self.date:
            title4 = ", on " + self.date.strftime("%b") + " " + self.date.strftime("%d") + ", " + self.date.strftime("%Y")
        title = title1 + title2 + titleseries + title3 + title4
        return title


class SermonFile(models.Model):
    """
    A file attached to a sermon (e.g. Powerpoint, Word etc...)
    """
    name = models.CharField(max_length=30, default="",
                            help_text="What does the file do? e.g. 'Sermon Outline', 'PowerPoint', 'Bible Study' etc...")
    file = FileField(max_length=255, blank=True,
                     help_text="Use the media manager to upload and select the")
    sermon = models.ForeignKey(Sermon)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
