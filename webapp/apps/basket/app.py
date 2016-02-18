#!/usr/bin/env python
# encoding: utf-8


from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from oscar.core.application import Application
from oscar.core.loading import get_class
from oscar.apps.basket.app import BasketApplication as CoreBasketApplication

from webapp.apps.basket.views import (buy_product, pay_order, order_cancel)

class BasketApplication(CoreBasketApplication):
    def get_urls(self):
        urls = [
            url(r'^buy/(?P<pk>\d+)/$', login_required(buy_product),
                name='buy'),
            url(r'^pay-order/(?P<pk>\d+)/$', login_required(pay_order),
                name='pay_order'),
            url(r'^order-cancel/(?P<pk>\d+)/$', login_required(order_cancel),
                name='order_cancel'),
        ]
        return self.post_process_urls(urls)


application = BasketApplication()
