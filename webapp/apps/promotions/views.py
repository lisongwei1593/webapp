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

ProductSearchForm = get_class('dashboard.catalogue.forms','ProductSearchForm')
Product = get_model('catalogue', 'product')
Category = get_model('catalogue', 'category')
get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
RollingAd = get_model('ad', 'RollingAd')
FlatPage = get_model('staticpages', 'FlatPageNew')

class HomeView(CoreHomeView):
    template_name = 'promotions/home.html'
    
    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        
        now = datetime.datetime.now().time()
        new_product_list = Product.objects.filter(is_on_shelves=True,opening_date__lte=datetime.datetime.now().date()).order_by('-date_updated')[:10]

        #新品上市消息
        ctx['news_product'] = FlatPage.objects.filter(category=3).order_by('-created_datetime')[:7]
        #购物须知
        ctx['buy_know'] = FlatPage.objects.filter(category=4).order_by('-created_datetime')[:5]
        #公告
        ctx['notice'] = FlatPage.objects.filter(category=2).order_by('-created_datetime')[:5]

        category_list = Category.objects.filter(depth=1).order_by('path')[:10]
        
        ctx['new_product_list'] = new_product_list

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
    
