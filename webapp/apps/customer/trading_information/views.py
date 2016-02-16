# -*- coding: utf-8 -*-
import datetime
import json
import traceback
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template import Context
from rest_framework.views import APIView
from oscar.core.loading import get_model
from django.core.urlresolvers import reverse



Product = get_model('catalogue', 'product')
ProductOrder = get_model('commission', 'ProductOrder')


def order_manage(request):
    user = request.user
    all_order = ProductOrder.objects.filter(user=user).order_by('-created_datetime')
    starttime = request.GET.get('starttime')
    if starttime:
        all_order = all_order.filter(created_datetime__gte=starttime)
    endtime = request.GET.get('endtime')
    if endtime:
        all_order = all_order.filter(created_datetime__lte=endtime)
    order = request.GET.get('order')
    if order:
        all_order = all_order.order_by(order)
    paginator = Paginator(all_order, 20)
    page = request.GET.get('page')
    try:
        all_order = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        all_order = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        all_order = paginator.page(paginator.num_pages)  # 取最后一页的记录
        
    for product_order in all_order:
        if product_order.pickup_type == 1:
            product_order.pickup_type='自提'
        elif product_order.pickup_type == 2:
            product_order.pickup_type='物流' 
        STATUS_CHOICES = ((0, u'未支付'), (1, u'支付中'), (2, u'支付成功'),
                      (3, u'支付失败'), (4, u'已关闭'), (5, u'已撤销'), (6, u'未发货'), (7, u'已发货'), (8, u'部分提货'), (9, u'已提货'))
        status_id = product_order.status
        product_order.status = STATUS_CHOICES[status_id][1]
        if product_order.effective == False:
            product_order.status = u"已取消"
    context = {'all_order': all_order,'page_title':u'订单管理','order':order,'frame_id':'order_manage'}
    return render(request, 'customer/trading_information/order_manage.html', context)


def order_detail(request):
    order_id = request.GET.get('order_id', '')
    if order_id:
        try:
            product_order = ProductOrder.objects.get(id=order_id)
            all_info = product_order.order_info.all()
            PICKUP_DETAIL_STATUS = (
                (1,'未提货'),
                (2,'已提货'),
                (3,'已驳回'),
                (4,'未发货'),
                (5,'已发货'),
                (6,'已评价'),
            )
            if product_order.status==2:
                for info in all_info:
                    status_id = int(info.order_pickup_detail.status) - 1
                    info.status = PICKUP_DETAIL_STATUS[status_id][1]
            else:
                STATUS_CHOICES = ((0, u'未支付'), (1, u'支付中'), (2, u'支付成功'),
                      (3, u'支付失败'), (4, u'已关闭'), (5, u'已撤销'), (6, u'未发货'), (7, u'已发货'), (8, u'部分提货'), (9, u'已提货'))
                status_id = product_order.status
                for info in all_info:
                    info.status = STATUS_CHOICES[status_id][1]
            current_template = get_template('customer/trading_information/partials/all_order_detail.html')
            context = {'all_info':all_info,'order':product_order}
            content_html = current_template.render(Context(context))
            payload = {'content_html': content_html, 'success': True}
            return HttpResponse(json.dumps(payload), content_type="application/json")
        except:
            traceback.print_exc()
            current_template = get_template('customer/trading_information/partials/all_order_detail.html')
            context = {'err_msg':'订单详情查询出错'}
            content_html = current_template.render(Context(context))
            payload = {'content_html': content_html, 'success': True}
            return HttpResponse(json.dumps(payload), content_type="application/json")
    else:
        return ""



