# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20160202_1639'),
        ('commission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='product',
            field=models.ForeignKey(related_name='order_product', default=1, verbose_name='\u5546\u54c1', to='catalogue.Product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='product_order',
            field=models.ForeignKey(related_name='order_info', default=1, verbose_name='\u8ba2\u5355\u53f7', to='commission.ProductOrder'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='confirmdeal',
            unique_together=set([('commission_buy_id', 'commission_sale_id')]),
        ),
    ]
