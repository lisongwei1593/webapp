# -*- coding: utf-8 -*-s

import os
import traceback
from django.db import models
from django.contrib.staticfiles.finders import find
from django.db.models.manager import Manager
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from oscar.apps.catalogue.abstract_models import (AbstractProduct,AbstractCategory,AbstractProductAttribute,
                                                  ProductAttributesContainer as CoreProductAttributesContainer)
from django.utils import timezone
from oscar.core.loading import get_model

from oscar.apps.catalogue.abstract_models import MissingProductImage as mpi
from oscar.core.compat import get_user_model


User = get_user_model()
WishLine = get_model('wishlists', 'Line')

class MissingProductImage(mpi):
    def symlink_missing_image(self, media_file_path):
        import platform
        if platform.system() in ['Windows']:
            static_file_path = find('oscar/img/%s' % self.name)
            if static_file_path is not None:
                if not os.path.exists(media_file_path):
                    open(media_file_path, "wb").write(open(static_file_path, "rb").read())
        else:
            return super(MissingProductImage, self).symlink_missing_image(self, media_file_path)


class MPProductAttributesContainer(CoreProductAttributesContainer):
    def __getattr__(self, name):
        if not name.startswith('_') and not self.initialised:
            values = self.get_values().select_related('attribute')
            for v in values:
                if isinstance(v.value, Manager):
                    setattr(self, v.attribute.code, v.value.all())
                else:
                    setattr(self, v.attribute.code, v.value)
            self.initialised = True
            return getattr(self, name)
        raise AttributeError(
            _("%(obj)s has no attribute named '%(attr)s'") % {
                'obj': self.product.get_product_class(), 'attr': name})


class Product(AbstractProduct):
    browse_num = models.BigIntegerField(default=0, verbose_name=u'浏览次数')
    is_on_shelves = models.BooleanField(default=True, verbose_name=u'是否上架')
    selection_reputation = models.BooleanField(default=False, verbose_name=u'口碑甄选')
    opening_date = models.DateField(default=timezone.now, verbose_name=u'上市时间')
    new_listing = models.BooleanField(default=False, verbose_name=u'新品上市')
    featured_hot = models.BooleanField(default=False, verbose_name=u'主推热卖')
    hot_deals = models.BooleanField(default=False, verbose_name=u'火热促销')
    product_long_image = models.ImageField(upload_to='images/products/%Y/%m/', verbose_name=u'广告长图', blank=True, null=True)
    trader = models.ForeignKey(User, blank=True, null=True, related_name='trader',
                                verbose_name=u'交易员')
    is_associate = models.BooleanField(default=False, verbose_name=u'是否关联')

    def __init__(self, *args, **kwargs):
        super(AbstractProduct, self).__init__(*args, **kwargs)
        self.attr = MPProductAttributesContainer(product=self)

    def primary_image_url(self):
        img = self.primary_image()
        if isinstance(img, ProductImage):
            return img.original
        elif isinstance(img, dict):
            return img['original']
        else:
            return ''

    def advertising_long_image(self):
        """
        返回商品的长广告图片地址
        """
        return self.product_long_image

    # 详情页中显示的当前价格
    def current_price_for_display(self):
        p = self.stockrecords.first()
        if p:
            return p.price_retail
        else:
            return ''

    # def get_missing_image(self):
    #     """
    #     Returns a missing image object.
    #     """
    #     # This class should have a 'name' property so it mimics the Django file
    #     # field.
    #     return MissingProductImage()

    def has_focused_by(self, user):
        if user.is_anonymous():
            return False
        return WishLine.objects.filter(wishlist__owner=user, product__pk=self.pk).exists()

    def _can_pickup(self):
        can_pickup = True
        try:
            StockProductConfig = get_model('commission', 'StockProductConfig')
            current_product_config = StockProductConfig.objects.get(product=self)
            if current_product_config.self_pick_or_express == 2:
                can_pickup = False
        except:
            can_pickup = True
        return can_pickup
    can_pickup = property(_can_pickup)

    def _get_min_snum(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            min_snum = current_product_config.min_snum
        except:
            min_snum = 0
        return min_snum
    min_snum = property(_get_min_snum)

    def _get_min_bnum(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            min_bnum = current_product_config.min_bnum
        except:
            min_bnum = 0
        return min_bnum
    min_bnum = property(_get_min_bnum)

    def _get_up_down_range(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            up_down_range = current_product_config.up_down_range
        except:
            up_down_range = 0
        return up_down_range
    up_down_range = property(_get_up_down_range)

    def _get_up_up_range(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            up_up_range = current_product_config.up_up_range
        except:
            up_up_range = 0
        return up_up_range
    up_up_range = property(_get_up_up_range)

    def _get_sale_num(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            sale_num = current_product_config.sale_num
        except:
            sale_num = 0
        return sale_num
    sale_num = property(_get_sale_num)

    def _get_express_price(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            express_price = current_product_config.express_price
        except:
            express_price = 0
        return express_price
    express_price = property(_get_express_price)

    def _get_pickup_price(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            pickup_price = current_product_config.pickup_price
        except:
            pickup_price = 0
        return pickup_price
    pickup_price = property(_get_pickup_price)

    def _get_max_num(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            max_num = current_product_config.max_num
        except:
            max_num = 0
        return max_num
    max_num = property(_get_max_num)

    def _get_once_max_num(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            once_max_num = current_product_config.once_max_num
        except:
            once_max_num = 0
        return once_max_num
    once_max_num = property(_get_once_max_num)

    def _get_opening_price(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            opening_price = current_product_config.opening_price
        except:
            opening_price = 0
        return opening_price
    opening_price = property(_get_opening_price)

    def _get_max_deal_num(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            max_deal_num = current_product_config.max_deal_num
        except:
            max_deal_num = 0
        return max_deal_num
    max_deal_num = property(_get_max_deal_num)

    def _get_max_buy_num(self):
        StockProductConfig = get_model('commission', 'StockProductConfig')
        try:
            current_product_config = StockProductConfig.objects.filter(product=self)[0]
            max_buy_num = current_product_config.max_buy_num
        except:
            max_buy_num = 0
        return max_buy_num
    max_buy_num = property(_get_max_buy_num)

    def _price_range(self):
        StockTicker = get_model('commission', 'StockTicker')
        product_config = self.stock_config_product
        try:
            current_stockticker = StockTicker.objects.filter(product=self).order_by('-created_datetime').first()
            if current_stockticker and current_stockticker.closing_price:
                product_price = current_stockticker.closing_price
            else:
                product_price = product_config.opening_price
        except:
            traceback.print_exc()
            product_price = 99999999
        max_price = "%.2f"%(float(product_price)*(1+float(product_config.ud_up_range)))
        min_price = "%.2f"%(float(product_price)*(1-float(product_config.ud_down_range)))
        product_price_range = [min_price,max_price]
        return product_price_range
    price_range = property(_price_range)

    
    def _image_url_or_none(self):
        try:
            img_url = self.primary_image().original.url
        except:
            img_url = ""
        return img_url
    img_url_or_none = property(_image_url_or_none)

    def save(self, *args, **kwargs):
        if self.trader:
            self.is_associate = True
        else:
            self.is_associate = False
        super(Product, self).save(*args, **kwargs)


class Category(AbstractCategory):
    product_class = models.ForeignKey(
        'catalogue.ProductClass', null=True, blank=True,
        verbose_name=_(u'分类类属性'), related_name="categories",
        help_text=_(u"选择分类的类属性，绑定分类商品属性值"))

    def get_child_category(self):
        """
        子类=商品，商品列表显示直接显示商品。
        """
        return self.product_set.filter(is_on_shelves=True)

    def get_product_class(self):
        """
        得到分类的商品类属性
        """
        p_class = self.product_class
        try:
            p_attributes = p_class.attributes.filter(search_filter = True)
        except:
            p_attributes = None

        return p_attributes

    def get_category_products(self):
        products = []
        for product in self.product_set.filter(is_on_shelves=True):
            products.append(product)
        if self.has_children():
            for child in self.get_children():
                for product in child.product_set.filter(is_on_shelves=True):
                    products.append(product)
                if child.has_children():
                    for c in child.get_children():
                        for product in c.product_set.filter(is_on_shelves=True):
                            products.append(product)
        return products


class ProductAttribute(AbstractProductAttribute):
    #该属性是否搜索
    search_filter = models.BooleanField(u'是否搜索', default=True,
                                        help_text = u'设置不需要搜索的属性值')
    index = models.IntegerField(blank=True, null=True, verbose_name=u'排序')

    def get_attributes(self):
        search_values = self.searchfilter_set.filter(chose = True).order_by('search_order')

        return search_values
    def __unicode__(self):
            return "%s %s" % (self.name,self.code)


class SearchFilter(models.Model):
    value_choise = (('>',u'以上'),('<',u'以下'))
    attribute = models.ForeignKey(
        'catalogue.ProductAttribute', verbose_name=_("Attribute"))
    search_value = models.CharField(u'搜索值',blank= True ,null = True,max_length=120,
                                    help_text = u'区间值设置成 eg:30度-40度')
    value_range = models.CharField(u'选择范围',blank = True , null = True ,choices=value_choise,max_length=120,
                                   help_text = u'不是范围的属性值为空')
    search_order = models.IntegerField(u'搜索值排列顺序',blank = True ,null = True )
    chose = models.BooleanField(u'选择该搜索值',default=True)

    class Meta :
        app_label = 'catalogue'
        ordering = ['attribute']
        verbose_name = u'搜索属性配置'
        verbose_name_plural = u'搜索属性配置'


from oscar.apps.catalogue.models import *  # noqa
