# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from oscar.apps.customer import app
import assets.urls
import trading_information.urls
import user_info.urls
import safety.urls
import receiving_address.urls
import finance.urls

class CustomerApplication(app.CustomerApplication):
    name = 'customer'

    def get_urls(self):
        urls = [
            # 账户资产
            url(r'^assets/', include(assets.urls)),
            # 交易信息
            url(r'^trading-information/', include(trading_information.urls)),
            # 个人信息
            url(r'^user_info/', include(user_info.urls)),
            # 收货地址
            url(r'^receiving-address/', include(receiving_address.urls)),
            # 账户安全
            url(r'^safety/', include(safety.urls)),
            # 签约支付
            url(r'^fin/', include(finance.urls)),
            # 收货地址
            ] + super(self.__class__, self).get_urls()

        return self.post_process_urls(urls)


application = CustomerApplication()
