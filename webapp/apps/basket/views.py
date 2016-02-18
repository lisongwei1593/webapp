# encoding: utf-8

import datetime
import json
import traceback

from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.shortcuts import redirect, render
from oscar.core.loading import get_model
from rest_framework.views import APIView

from webapp.apps.commission.models import ProductOrder, OrderInfo


Line = get_model('basket', 'Line')
Product = get_model('catalogue', 'Product')
Category = get_model('catalogue','Category')
Partner = get_model('partner', 'Partner')


def buy_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product_order = ProductOrder()
        product_order.user=request.user
        product_order.amount=product.stockrecords.first().price_retail
        product_order.status=0
        product_order.product_price = product.stockrecords.first().price_retail
        product_order.express_fee = 0
        product_order.pickup_fee = 0
        product_order.detail = product.title
        product_order.custom_save()
        OrderInfo.objects.create(product_order=product_order,product=product,product_num=1,price=product.stockrecords.first().price_retail)
        context = {'product_order':product_order}
        return render(request, 'basket/pay_order.html', context)
    except:
        traceback.print_exc()
        return render(request, 'basket/order_error.html','')
        
        
def pay_order(request, pk):
    if request.method == 'GET':
        product_order = ProductOrder.objects.get(id=pk)
        context = {'product_order':product_order}
        return render(request, 'basket/pay_order.html', context)
            
            
#取消订单
def order_cancel(request, pk):
    product_order = ProductOrder.objects.get(id=pk)
    product_order.effective = False
    product_order.save()
    return redirect('customer:order_manage')

