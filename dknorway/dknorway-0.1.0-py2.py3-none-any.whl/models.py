# -*- coding: utf-8 -*-

"""Models used for looking up poststed from postnr.
   Updated by ./posten_postnrimport.py
"""

# pylint: disable=W0232,R0903
# W0232: META has no __init__
# R0903: too few public methods


from django.db import models


class Fylke(models.Model):
    "Model for all fylker in Norway."
    nr = models.CharField(max_length=2, primary_key=True)
    navn = models.CharField(max_length=40)

    def __unicode__(self):
        return self.navn

    class Meta:
        "Meta options for :model:`Fylke`."
        verbose_name_plural = 'Fylker'
        ordering = ['nr']
    

class Kommune(models.Model):
    "Model for all kommuner in Norway."
    kode = models.CharField(max_length=4)
    navn = models.CharField(max_length=30)

    def __unicode__(self):
        return '%s (%s)' % (self.navn, self.fylke)

    @property
    def fylke(self):
        "Which fylke does the Kommune belong to?"
        return Fylke.objects.get(nr=self.kode[:2])

    class Meta:
        "Meta options for :model:`Kommune`."
        verbose_name_plural = 'Kommuner'
        ordering = ['kode']
    

class PostSted(models.Model):
    "A poststed as defined by the Norwegian postal service."
    postnummer = models.CharField(max_length=4)
    poststed = models.CharField(max_length=35)
    kommune = models.ForeignKey(Kommune, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return '%s %s' % (self.postnummer, self.poststed)

    @staticmethod
    def get(nr):
        "Convenience function to get the :model:`PostSted` from postnr."
        try:
            ps = PostSted.objects.get(postnummer=nr)
            return ps.poststed
        except PostSted.DoesNotExist:
            return u''
        
    class Meta:
        "Meta options for `model`:PostSted."
        verbose_name_plural = 'Poststed'
