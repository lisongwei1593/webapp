# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from oscar.core.loading import get_class
from webapp.apps.customer.assets.views import get_user_income

assets_view = get_class('customer.assets.views', 'AssetsView')


urlpatterns = (
      url(r'^$',
        login_required(assets_view.as_view()),
        name='assets'),
      url(r'^getuserincome/$',get_user_income,name = 'getuserincome'),

)

