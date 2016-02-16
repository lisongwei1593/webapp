# -*- coding: utf-8 -*-s

from django.db import models

from django.contrib.auth.models import User
from oscar.core.loading import get_model



Product = get_model('catalogue', 'Product')


PICKUP_TYPE = (
    (1, '购买'),
    (2, '进货'),
    (3, '全部'),
)


class PickupProvisionalRecord(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    product = models.ForeignKey(Product, verbose_name=u'商品')
    quantity = models.IntegerField(default=1, verbose_name=u'提货数量')
    max_quantity = models.IntegerField(verbose_name=u'货物余量')
    available = models.BooleanField(default=False, verbose_name=u'是否可用')
    pickup_type = models.IntegerField(default=1,
                                      choices=PICKUP_TYPE, verbose_name=u'提货类型')


    class Meta:
        verbose_name = verbose_name_plural = u'提货临时记录'
        unique_together = ('user', 'product')

    def __unicode__(self):
        return self.user.username
