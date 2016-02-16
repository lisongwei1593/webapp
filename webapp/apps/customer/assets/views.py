 # -*- coding: utf-8 -*-
from __future__ import division

import json
from collections import defaultdict
from datetime import datetime, timedelta

from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import  connection
from django.db.models import Sum, Count, Q, F, FloatField
from django.db.models.functions import Coalesce
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.apps.customer.assets.utils import AssetsUtil
from webapp.apps.customer.safety.utils import convert_none_or_empty_to_0


class AssetsView(APIView):
    tpl = 'customer/assets/account_assets.html'
    __row_per_page = 20

    def get(self, request, *args, **kwargs):
        user = request.user
        data = request.GET

        period_type = data.get('period_type')
        flag = data.get('flag')
        flag = 1 if flag != '2' else 2
        ctx = {'flag': flag, 'period_type': period_type}

        start_time, end_time = self.get_date_range(period_type)

        period_cond = 'period_type={}'.format(period_type) if period_type else ''
        if period_type == 'start-end':
            if start_time:
                period_cond += '&start_date={}'.format(start_time)
            if end_time:
                period_cond += '&end_date={}'.format(end_time)
            if period_cond.startswith('&'):
                period_cond =period_cond[1:]
            ctx['start_date'] = start_time
            ctx['end_date'] = end_time
        ctx['period_cond'] = period_cond
        # ctx = {'flag': flag, 'period_type': period_type, 'start_date': start_time, 'end_date': end_time, 'period_cond': period_cond}

        try:
            page_idx = data.get('page')
            if not page_idx:
                page_idx = 1
            else:
                page_idx = int(page_idx)
        except ValueError:
            return Response(status=http_status.HTTP_400_BAD_REQUEST)

        is_verified = True if hasattr(user, 'userprofile') and user.userprofile.audit_status else False

        ctx['user'] = {'is_verified': is_verified, 'name': user.username, 'fund_acc_id': user.userprofile.uid}

        if end_time and period_type == 'start-end':
            end_time = (parser.parse(end_time) + timedelta(days=1)).strftime('%Y-%m-%d')

        ctx['frame_id'] = 'assets'

        return render(request,self.tpl, ctx)

    def get_date_range(self, period_type):
        start_time, end_time = None, None
        if period_type == 'start-end':
            start_time, end_time = self.request.GET.get('start_date'), self.request.GET.get('end_date')

        elif period_type == '1_month':
            start_time, end_time = datetime.today() - relativedelta(months=1), datetime.today()
        elif period_type == '3_month':
            start_time, end_time = datetime.today() - relativedelta(months=3), datetime.today()
        elif period_type == '1_year':
            start_time, end_time = datetime.today() - relativedelta(years=1), datetime.today()
        return start_time, end_time


@login_required
def get_user_income(request):
    user = request.user
    result = {}
    
    try :
        #=======================================================================
        # #昨日收益
        # today = datetime.today().date()
        # yesterday = today - timedelta(days=1)
        # yesterday_icome = UserAssetDailyReport.objects.filter(target_date=yesterday, user=user).values('income')
        # if yesterday_icome :
        #     yesterday_icome = str(yesterday_icome[0]['income'])
        # else :
        #     yesterday_icome = "0.0"
        # #累计收益
        # total_icome = UserAssetDailyReport.objects.filter(user=user).aggregate(Sum('income')).values()
        # if total_icome :
        #     total_icome = str(total_icome[0])
        # else :
        #     total_icome = "0.0"
        #=======================================================================
        #昨日收益
        yesterday_icome = AssetsUtil.get_profit(user.id)[1]
        if yesterday_icome:
            yesterday_icome = yesterday_icome
        else :
            yesterday_icome =0.00
        #累计收益
        total_icome = AssetsUtil.get_profit(user.id)[0]
        if total_icome :
            total_icome = total_icome
        else:
            total_icome = 0.00
        
    except :
        pass
    
    result = {'yesterday_icome':yesterday_icome,
              'total_icome' :total_icome,
              }
    
    return HttpResponse(json.dumps(result),content_type="application/json")