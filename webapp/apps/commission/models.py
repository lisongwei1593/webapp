# -*- coding: utf-8 -*-s

from django.contrib.auth.models import User
from django.db import models
from oscar.core.loading import get_model


Product = get_model('catalogue', 'Product')
Category = get_model('catalogue','Category')

PICKUP_TYPE = (
        (1,'自提'),
        (2,'物流'),
    )


class ProductOrder(models.Model):
    """
    订单
    """
    STATUS_CHOICES = ((0, u'未支付'), (1, u'支付中'), (2, u'支付成功'),
                      (3, u'支付失败'), (4, u'已关闭'), (5, u'已撤销'), (6, u'未发货'), (7, u'已发货'), (8, u'部分提货'), (9, u'已提货'))
    TYPE_CHOICES = ((1, u'购买'), (2, u'进货'), (3, u'出售'))
    PAY_TYPE = ((1, u'余额'), (2, u'第三方'))
    order_no = models.CharField(max_length=32, unique=True)  # 订单号
    user = models.ForeignKey(User)
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=u'总价')   # 总价
    product_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=u'产品费用')
    express_fee = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=u'快递费')
    pickup_fee = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=u'杂费')
    description = models.CharField(max_length=200, blank=True, default='', verbose_name=u'商品描述')    # 订单商品简要描述
    detail = models.CharField(max_length=500, blank=True, default='',  verbose_name=u'商品详情')    #订单商品明细列表

    trade_type = models.SmallIntegerField(choices=TYPE_CHOICES, default=1)      # 订单类型
    pickup_type = models.SmallIntegerField(choices=PICKUP_TYPE, default=1)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)       # 订单状态
    pay_type = models.SmallIntegerField(choices=PAY_TYPE, blank=True, null=True) 
    addr = models.CharField(blank=True, null=True, default='', max_length=1000, verbose_name=u'订单地址')
    effective = models.BooleanField(default=True, verbose_name=u'是否有效')
    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_datetime = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

    class Meta:
        verbose_name = verbose_name_plural = u'订单'

    def __unicode__(self):
            return self.order_no

    def has_payed(self):
        return self.status == 2

    def is_paying(self):
        return self.status == 1

    def custom_save(self, *args, **kwargs):
        super(ProductOrder, self).save(*args, **kwargs)
        self.order_no = int(self.id) + 100000000000
        self.save()
        

class OrderInfo(models.Model):
    product_order = models.ForeignKey(ProductOrder, related_name='order_info', db_index=True,
                             verbose_name=u'订单号')
    product = models.ForeignKey(Product, related_name='order_product', db_index=True,
                                 verbose_name=u'商品')
    product_num = models.IntegerField(default=0, verbose_name=u'商品数量')
    price = models.FloatField(default=0,  verbose_name=u'订单商品价格')
    class Meta:
        verbose_name = verbose_name_plural = u'订单信息'

    def __unicode__(self):
            return self.product_order.order_no







