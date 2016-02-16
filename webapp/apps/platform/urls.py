# encoding: utf-8


from django.conf.urls import patterns, url

urlpatterns = patterns('webapp.apps.platform.views',
    url(r'^stock-enter/$', 'stock_enter', name='stock_enter'),
)
