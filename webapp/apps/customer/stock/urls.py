# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from webapp.apps.customer.stock.views import (stock, pickup_set, pickup_apply,
                                             add_pickup_addr, add_receiving_addr,
                                             pickup_store_check,
                                             pickup_quantity_set, pickup_success)


urlpatterns = (
)

