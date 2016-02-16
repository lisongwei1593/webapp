
from django.contrib import admin

from webapp.apps.commission.models import (SystemConfig,ProductOrder,
                                          OrderInfo)

class PickupAddrAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'province', 'city', 'district',
                    'addr', 'lng', 'lat')
    filter_horizontal = ('staff',)


class UserPickupAddrAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pickup_addr', 'is_default')


class PickupListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pickup_no', 'pickup_type', 'status',
                    'pickup_fee', 'express_fee')




class UserAssetDailyReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_date','start_balance','income','locked','total')




class ConfirmDealAdmin(admin.ModelAdmin):
    list_display = ('commission_buy_id', 'commission_sale_id')
    
    
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'user','amount','description','detail')
    
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('product_order','product','product_num','price')

admin.site.register(SystemConfig)
admin.site.register(ProductOrder, ProductOrderAdmin)
