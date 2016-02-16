# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from webapp.apps.customer.trading_information.views import order_manage, order_detail

urlpatterns = (
      url(r'^order-manage/$', login_required(order_manage), name='order_manage'),
      url(r'^order-detail/$', login_required(order_detail), name='order_detail'),
)

