# -*- coding: utf-8 -*-
from __future__ import division
from collections import defaultdict
from datetime import datetime, timedelta
from django.db.models import Sum, Case, When, Q, F, FloatField
from django.db.models.functions import Coalesce
from webapp.apps.customer.safety.common_const import Const


def mask_bank_card_no(no):
    if no:
        s = '*'*(len(no)-4) + no[-4:]
        r = s[:4] + ' '
        for i in range(1, (len(no)+3)//4):
            r += s[4*i:4*(i+1)] + ' '
        return r
    return no


def mask_id_card_no(id):

    return '{}***{}'.format(id[:9], id[-3:]) if id else ''


def is_valid_bank_card_num(num):
    r = num.replace(' ','')
    return 20 > len(r) > 10 and r.isdigit()


def is_valid_mobile(num):
    prefix=['130','131','132','133','134','135','136','137','138','139',
                 '150','151','152','153','156','158','159','170', '172',
                 '178','181', '182','183','185','186','187','188','189']

    return num and len(num) == 11 and num.isdigit() and num[0:3] in prefix


class _BankData(Const):
    BANK_IMG_URLS = {
                        # '中国工商银行': 'images/ABC.png',
                        u'中国农业银行': u'images/ABC.png',
                        # '中国银行': 'images/',
                        u'中国建设银行': u'images/CCB.png',
                        # '交通银行': 'images/',
                        # '中国邮政银行': 'images/',
                        u'招商银行': u'images/CMB.png',}
    BANK_CHOICES = set(BANK_IMG_URLS.keys())

BankData = _BankData()


def is_valid_bank(name):
    return name in BankData.BANK_CHOICES


class AssetsUtil():
    @staticmethod

    @staticmethod
    def get_profit(user_id):
        """
        返回指定用户累计收益(截至昨天)、昨天收益
        :param user_id:
        :return: (累计收益, 昨天收益)
        """

        total_income_up_to_yesterday = AssetsUtil.get_profit_up_to_thd_day(user_id, datetime.today() - timedelta(days=1))
        total_income_up_to_the_day_before_yesterday = AssetsUtil.get_profit_up_to_thd_day(user_id, datetime.today() - timedelta(days=2))
        yesterday_income = total_income_up_to_yesterday - total_income_up_to_the_day_before_yesterday

        return total_income_up_to_yesterday, yesterday_income
