from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required



urlpatterns = patterns('webapp.apps.helper.views',
    url(r'^$', 'helper_index', name='helper_index'),
)
