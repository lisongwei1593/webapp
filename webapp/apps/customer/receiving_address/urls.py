# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from webapp.apps.customer.receiving_address.views import get_location


urlpatterns = (
      url(r'^get-location/$', login_required(get_location), name='get_location'),
)

