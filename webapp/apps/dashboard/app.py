import staticpages.urls

from django.conf.urls import url, include

from oscar.core.loading import get_class
from oscar.apps.dashboard.app import DashboardApplication as da

from webapp.apps.accounts.decorators import permission_required
from webapp.apps.dashboard import views

class DashboardApplication(da):
    ad_app = get_class('dashboard.ad.app', 'application')
    permission_app = get_class('dashboard.permission.app', 'application')

    login_view = views.LoginView
    logout_view = views.LogoutView

    def get_urls(self):
        # urls = super(DashboardApplication, self).get_urls()
        urls = [
            url(r'^$', permission_required(['dashboard_admin','ISP'])(self.index_view.as_view()), name='index'),
            url(r'^ad/', include(self.ad_app.urls)),
            url(r'^permission/', include(self.permission_app.urls)),
            url(r'^catalogue/', include(self.catalogue_app.urls)),

            url(r'^login/$', self.login_view.as_view(), name='dashboard-login'),
            url(r'^logout/$', self.logout_view.as_view(), name='dashboard-logout'),

            url(r'^staticpages/', include(staticpages.urls)),
        ]

        return self.post_process_urls(urls)


application = DashboardApplication()
