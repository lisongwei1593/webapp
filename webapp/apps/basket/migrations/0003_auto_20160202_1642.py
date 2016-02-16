# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oscar.core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0001_initial'),
        ('basket', '0002_auto_20140827_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='vouchers',
            field=models.ManyToManyField(to='voucher.Voucher', verbose_name='Vouchers', blank=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='price_currency',
            field=models.CharField(default=oscar.core.utils.get_default_currency, max_length=12, verbose_name='Currency'),
        ),
    ]
