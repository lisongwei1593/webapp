# -*- coding: utf-8 -*-s

import datetime
import traceback
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.db.models import Sum
from oscar.core.loading import get_model


Product = get_model('catalogue', 'Product')
Category = get_model('catalogue','Category')

COMMISSION_BUY_TYPE = (
        (1, '购买'),
        (2, '进货'),
    )
COMMISSION_SALE_TYPE = (
        (1, '出售'),
    )
TRADE_COMPLETE_TYPE = (
        (1, '购买'),
        (2, '进货'),
    )
SELF_PICK_OR_EXPRESS = (
        (1,'仅自提'),
        (2,'仅物流'),
        (3,'自提和物流'),
    )
COMMISSION_STATUS_CHOICES = (
        (1,'待成交'),
        (2,'部分成交'),
        (3,'成交'),
        (4,'撤单')
    )
COMMCAL_TYPEDATA_CHOICES = (
        (1,'定量'),
        (2,'比例')
    )
UD_STY_CHOICES = (
        (1,'定量'),
        (2,'比例')
    )
MONEY_CHANGE_TRADE_TYPE = (
        (1,'充值'),
        (2,'提现'),
        (3,'购买冻结'),
        (4,'购买解冻'),
        (5,'购买成交'),
        (6,'进货冻结'),
        (7,'进货解冻'),
        (8,'进货成交'),
        (9,'出售'),
        (10,'提货冻结'),
        (11,'提货驳回'),
        (12,'提货完成'),
        (13,'撤单'),
        (14,'闭市撤单'),
        (15,'卖手续费'),
        (16,'订单快递费'),
        (17,'订单杂费'),
        (18,'购买快递费'),
        (19,'购买杂费'),
        (20,'购买结余'),
        (21,'收取手续费'),
        
    )
MONEY_CHANGE_STATUS = (
        (1,'进行中'),
        (2,'成功'),
        (3,'失败'),
    )
PICKUP_TYPE = (
        (1,'自提'),
        (2,'物流'),
    )
PICKUP_ADDR_TYPE = (
        (1,'自提'),
        (2,'自提点代运'),
        (3,'厂商发货'),
    )
PICKUP_DETAIL_STATUS = (
        (1,'未提货'),
        (2,'已提货'),
        (3,'已驳回'),
        (4,'未发货'),
        (5,'已发货'),
        (6,'已评价'),
    )
DEAL_FEE_TYPE = (
        (1, '购买'),
        (2, '出售'),
    )


class SystemConfig(models.Model):
    is_open = models.BooleanField(default=True, verbose_name=u'是否开市')
    auto_open = models.BooleanField(default=False, verbose_name=u'自动开市')
    bank_start_time = models.TimeField(verbose_name=u'银行开始时间')
    bank_end_time = models.TimeField(verbose_name=u'银行关闭时间')
    buy_price_rate = models.FloatField(default=1,verbose_name=u'购买费率')
    platform_user = models.CharField(max_length=30, verbose_name=u'平台账户用户名')
    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_datetime = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

    class Meta:
        verbose_name = verbose_name_plural = u'系统配置表'


class UserBank(models.Model):
    user = models.ForeignKey(User, related_name='bank_user', db_index=True,
                             verbose_name=u'用户')
    bank_name = models.CharField(max_length=255, verbose_name=u'银行名')
    bank_account = models.CharField(max_length=255, verbose_name=u'银行账号')
    tel = models.CharField(blank=True, null=True, max_length=30, verbose_name=u'电话')
    is_enable = models.BooleanField(default=False, verbose_name=u'是否启用')
    desc = models.CharField(default='', max_length=1000, verbose_name=u'备注')
    client_no = models.CharField(default='', max_length=100, verbose_name=u'银行客户号')
    client_name = models.CharField(default='', max_length=100, verbose_name=u'银行客户姓名')
    is_business_account = models.BooleanField(default=False, verbose_name=u'是否对公账户')
    is_rescinded = models.BooleanField(default=False, verbose_name=u'是否解约')
    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_datetime = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

    class Meta:
        verbose_name = verbose_name_plural = u'用户银行卡表'

    def __unicode__(self):
            return self.user.username





REPLAY_STATS=(
              ('1',u'未审核'),('2','已驳回'),('3',u'仓库已审核'),('4',u'已入库')
              )


class DealFeeCollect(models.Model):
    buy_deal_fee = models.FloatField(default=0, blank=True, null=True, verbose_name=u'买手续费')
    sale_deal_fee = models.FloatField(default=0, blank=True, null=True, verbose_name=u'卖手续费')
    created_date = models.DateField(auto_now_add=True, verbose_name=u'创建日期')
    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modified_datetime = models.DateTimeField(auto_now=True, db_index=True,
                                             verbose_name=u'修改时间')



class ConfirmDeal(models.Model):
    commission_buy_id = models.CharField(max_length=255, verbose_name=u'委托买编号')
    commission_sale_id = models.CharField(max_length=255, verbose_name=u'委托卖编号')

    class Meta:
        verbose_name = verbose_name_plural = u'交易匹配表'
        unique_together = ('commission_buy_id', 'commission_sale_id')





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







