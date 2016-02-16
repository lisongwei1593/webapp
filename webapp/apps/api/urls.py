# coding=utf-8
from django.conf.urls import patterns, url, include
from rest_framework.authentication import BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from webapp.apps.api.views import (APIRegisterView, APIGetsmscodeView,
    APITestTokenView, APILoginView, APIGetimgverifycodeView, APIFindpwdView,
    APIResetpwdView, APICheckusernameView, APIUpdateusernameView, 
    APIGetOrdersView, APIGetOrderDetailView, APICancelOrderView)

urlpatterns = patterns('',
    url(r'^auth/', 'rest_framework_jwt.views.obtain_jwt_token', name='api_auth'),
)

urlpatterns += patterns('webapp.apps.api.views',
    url(r'^test/$', APITestTokenView.as_view(authentication_classes=[JSONWebTokenAuthentication]), name='test'),
    # about account
    url(r'^getsmscode/$', APIGetsmscodeView.as_view(authentication_classes=[BasicAuthentication]), name='api_getsmscode'),
    url(r'^getimgverifycode/$', APIGetimgverifycodeView.as_view(authentication_classes=[BasicAuthentication]), name='api_getimgverifycode'),
    url(r'^findpwd/$', APIFindpwdView.as_view(authentication_classes=[BasicAuthentication]), name='api_findpwd'),
    url(r'^resetpwd/$', APIResetpwdView.as_view(authentication_classes=[BasicAuthentication]), name='api_resetpwd'),
    url(r'^checkusername/$', APICheckusernameView.as_view(authentication_classes=[JSONWebTokenAuthentication]), name='api_checkusername'),
    url(r'^updateusername/$', APIUpdateusernameView.as_view(authentication_classes=[JSONWebTokenAuthentication]), name='api_updateusername'),
    url(r'^register/$', APIRegisterView.as_view(authentication_classes=[BasicAuthentication]), name='api_register'),
    url(r'^login/$', APILoginView.as_view(authentication_classes=[BasicAuthentication]), name='api_login'),

    url(r'^getorderdetail/(?P<order_id>\d+)/$', APIGetOrderDetailView.as_view(authentication_classes=[JSONWebTokenAuthentication]), name='api_getorderdetail'),
    url(r'^cancelorder/(?P<order_id>\d+)/$', APICancelOrderView.as_view(authentication_classes=[JSONWebTokenAuthentication]), name='api_cancelorder'),
    url(r'^getorders/$', APIGetOrdersView.as_view(authentication_classes=[JSONWebTokenAuthentication]), name='api_getorders'),
)
