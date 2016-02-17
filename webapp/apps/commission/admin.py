
from django.contrib import admin

from webapp.apps.commission.models import (ProductOrder,
                                          OrderInfo)

    
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'user','amount','description','detail')
    
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('product_order','product','product_num','price')

admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
