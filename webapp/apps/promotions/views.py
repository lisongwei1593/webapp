# -*- coding: utf-8 -*-s

import datetime
import json
import random

from django.http.response import HttpResponse
from django.shortcuts import render_to_response, get_list_or_404
from django.template.context import RequestContext
from django.views.generic.base import TemplateView
from django.views import generic
from django.db.models import Sum, Max, Min
from oscar.apps.promotions.views import HomeView as CoreHomeView
from oscar.core.loading import get_model, get_class
from webapp.apps.catalogue.utils import open_close_date

ProductSearchForm = get_class('dashboard.catalogue.forms','ProductSearchForm')
Product = get_model('catalogue', 'product')
Category = get_model('catalogue', 'category')
get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
RollingAd = get_model('ad', 'RollingAd')
FlatPage = get_model('staticpages', 'FlatPageNew')
SystemConfig = get_model('commission', 'SystemConfig')

class HomeView(CoreHomeView):
    template_name = 'promotions/home.html'
    
    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        
        system_config = SystemConfig.objects.first()
        now = datetime.datetime.now().time()
        open_time = system_config.bank_start_time.strftime('%H:%M')
        close_time = system_config.bank_end_time.strftime('%H:%M')
        if system_config.bank_start_time < now and now < system_config.bank_end_time:
            open_close_msg = u"开市(当日%s-%s)"%(open_time,close_time)
            ctx['open_or_close'] = True
        else:
            open_close_msg = u"闭市(%s-次日%s)"%(close_time,open_time)
            ctx['open_or_close'] = False
        ctx['open_close_msg'] = open_close_msg
        new_product_list = Product.objects.filter(is_on_shelves=True,opening_date__lte=datetime.datetime.now().date()).order_by('-date_updated')[:10]
        ##shuiji
        reputation_list = Product.objects.filter(selection_reputation = True,is_on_shelves = True,opening_date__lte=datetime.datetime.now().date()).order_by('-date_updated')[:11]

        #新品上市消息
        ctx['news_product'] = FlatPage.objects.filter(category=3).order_by('-created_datetime')[:7]
        #购物须知
        ctx['buy_know'] = FlatPage.objects.filter(category=4).order_by('-created_datetime')[:5]
        #公告
        ctx['notice'] = FlatPage.objects.filter(category=2).order_by('-created_datetime')[:5]

        category_list = Category.objects.filter(depth=1).order_by('path')[:10]
        
        ctx['new_product_list'] = new_product_list

        ctx['reputation_list'] = reputation_list
        ctx['category_list'] = category_list
        ad_list = RollingAd.objects.filter(valid=True)
        ctx['rolling_ad_list'] = ad_list.filter(position='home_ad') # 轮播广告 by lwj 修改：包括页面其它广告
        ctx['zhutui_ad_list'] = ad_list.filter(position = 'home_ad_3').first()
        ctx['huore_ad_list'] = ad_list.filter(position = 'home_ad_4').first()
        
        now_time = datetime.datetime.today()
        ctx['now_hour'] = now_time.hour
        ctx['now_minute'] = now_time.minute
        
        return ctx


class SearchView(TemplateView):
    template_name = 'promotions/search_form.html'

class TodayNewView(TemplateView):
    template_name = 'promotions/today_new_product.html'
    
    def get_context_data(self, **kwargs):
        ctx = super(TodayNewView, self).get_context_data(**kwargs)
        
        category_list = Category.objects.filter(depth=1).order_by('path')[:10]
        ctx['category_list'] =category_list
        ctx['open_or_close'] = open_close_date()[0]
        ctx['open_close_msg'] = open_close_date()[1]
        return ctx

#包括 新品上市,购物须知,公告
class NewsProductView(generic.ListView):
    template_name = 'promotions/news_product.html'
    paginate_by = 50
    context_object_name = 'news_list'

    def get_queryset(self):
        queryset = FlatPage.objects.all()
        self.flag = self.request.GET.get('flag','3')

        if self.flag == '3':
            queryset = queryset.filter(category=3).order_by('-created_datetime')
        if self.flag == '4':
            queryset = queryset.filter(category=4).order_by('-created_datetime')
        if self.flag == '2':
            queryset = queryset.filter(category=2).order_by('-created_datetime')

        return queryset


    def get_context_data(self, **kwargs):
        ctx = super(NewsProductView, self).get_context_data(**kwargs)
        ctx['flag'] = self.flag

        return ctx
 

class NewsProductDetailView(TemplateView):
    template_name = 'promotions/news_product_detail.html'   

    def get_context_data(self, **kwargs):
        ctx = super(NewsProductDetailView, self).get_context_data(**kwargs)

        try:
            #新品上市消息,购物须知,公告
            ctx['news_product_detail'] = FlatPage.objects.get(pk=kwargs.get("pk"))
        except:
            pass
        return ctx
    

#品牌汇
class BrandGatherView(TemplateView):
    template_name = 'promotions/brand_gather.html'
    
    def get_context_data(self, **kwargs):
        ctx = super(BrandGatherView, self).get_context_data(**kwargs)
        
        product_list = Product.objects.filter(is_on_shelves=True,opening_date__lte=datetime.datetime.now().date())[:20]
        category_list = Category.objects.filter(depth=1).order_by('path')[:10]
        ctx['product_list'] = product_list
        ctx['category_list'] =category_list
        ctx['open_or_close'] = open_close_date()[0]
        ctx['open_close_msg'] = open_close_date()[1]
        return ctx
    