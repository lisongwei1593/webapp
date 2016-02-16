# -*- coding: utf-8 -*-s

from django.db import models

class Province(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'省名')
    slug_name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = u'省'

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'城市名')
    slug_name = models.CharField(max_length=64)
    province = models.ForeignKey(Province, verbose_name=u'所属省')
    lat = models.FloatField(default=0, blank=True, null=True, max_length=15, verbose_name=u'纬度')
    lng = models.FloatField(default=0, blank=True, null=True, max_length=15, verbose_name=u'经度')

    class Meta:
        verbose_name = verbose_name_plural = u'城市'
        unique_together = (('slug_name', 'province'),)

    def __unicode__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'区名')
    slug_name = models.CharField(max_length=64)
    city = models.ForeignKey(City, verbose_name=u'所属城市')
    lat = models.FloatField(default=0, blank=True, null=True, max_length=15, verbose_name=u'纬度')
    lng = models.FloatField(default=0, blank=True, null=True, max_length=15, verbose_name=u'经度')

    class Meta:
        verbose_name = verbose_name_plural = u'区'
        unique_together = (('slug_name', 'city'),)

    def __unicode__(self):
        return self.name



from oscar.apps.address.models import *  # noqa
