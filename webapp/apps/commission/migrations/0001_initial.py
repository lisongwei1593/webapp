# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmDeal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commission_buy_id', models.CharField(max_length=255, verbose_name='\u59d4\u6258\u4e70\u7f16\u53f7')),
                ('commission_sale_id', models.CharField(max_length=255, verbose_name='\u59d4\u6258\u5356\u7f16\u53f7')),
            ],
            options={
                'verbose_name': '\u4ea4\u6613\u5339\u914d\u8868',
                'verbose_name_plural': '\u4ea4\u6613\u5339\u914d\u8868',
            },
        ),
        migrations.CreateModel(
            name='DealFeeCollect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buy_deal_fee', models.FloatField(default=0, null=True, verbose_name='\u4e70\u624b\u7eed\u8d39', blank=True)),
                ('sale_deal_fee', models.FloatField(default=0, null=True, verbose_name='\u5356\u624b\u7eed\u8d39', blank=True)),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='\u521b\u5efa\u65e5\u671f')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modified_datetime', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_num', models.IntegerField(default=0, verbose_name='\u5546\u54c1\u6570\u91cf')),
                ('price', models.FloatField(default=0, verbose_name='\u8ba2\u5355\u5546\u54c1\u4ef7\u683c')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u4fe1\u606f',
                'verbose_name_plural': '\u8ba2\u5355\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_no', models.CharField(unique=True, max_length=32)),
                ('amount', models.DecimalField(verbose_name='\u603b\u4ef7', max_digits=15, decimal_places=2)),
                ('product_price', models.DecimalField(verbose_name='\u4ea7\u54c1\u8d39\u7528', max_digits=15, decimal_places=2)),
                ('express_fee', models.DecimalField(verbose_name='\u5feb\u9012\u8d39', max_digits=15, decimal_places=2)),
                ('pickup_fee', models.DecimalField(verbose_name='\u6742\u8d39', max_digits=15, decimal_places=2)),
                ('description', models.CharField(default=b'', max_length=200, verbose_name='\u5546\u54c1\u63cf\u8ff0', blank=True)),
                ('detail', models.CharField(default=b'', max_length=500, verbose_name='\u5546\u54c1\u8be6\u60c5', blank=True)),
                ('trade_type', models.SmallIntegerField(default=1, choices=[(1, '\u8d2d\u4e70'), (2, '\u8fdb\u8d27'), (3, '\u51fa\u552e')])),
                ('pickup_type', models.SmallIntegerField(default=1, choices=[(1, b'\xe8\x87\xaa\xe6\x8f\x90'), (2, b'\xe7\x89\xa9\xe6\xb5\x81')])),
                ('status', models.SmallIntegerField(choices=[(0, '\u672a\u652f\u4ed8'), (1, '\u652f\u4ed8\u4e2d'), (2, '\u652f\u4ed8\u6210\u529f'), (3, '\u652f\u4ed8\u5931\u8d25'), (4, '\u5df2\u5173\u95ed'), (5, '\u5df2\u64a4\u9500'), (6, '\u672a\u53d1\u8d27'), (7, '\u5df2\u53d1\u8d27'), (8, '\u90e8\u5206\u63d0\u8d27'), (9, '\u5df2\u63d0\u8d27')])),
                ('pay_type', models.SmallIntegerField(blank=True, null=True, choices=[(1, '\u4f59\u989d'), (2, '\u7b2c\u4e09\u65b9')])),
                ('addr', models.CharField(default=b'', max_length=1000, null=True, verbose_name='\u8ba2\u5355\u5730\u5740', blank=True)),
                ('effective', models.BooleanField(default=True, verbose_name='\u662f\u5426\u6709\u6548')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modified_datetime', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u8ba2\u5355',
                'verbose_name_plural': '\u8ba2\u5355',
            },
        ),
        migrations.CreateModel(
            name='SystemConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_open', models.BooleanField(default=True, verbose_name='\u662f\u5426\u5f00\u5e02')),
                ('auto_open', models.BooleanField(default=False, verbose_name='\u81ea\u52a8\u5f00\u5e02')),
                ('bank_start_time', models.TimeField(verbose_name='\u94f6\u884c\u5f00\u59cb\u65f6\u95f4')),
                ('bank_end_time', models.TimeField(verbose_name='\u94f6\u884c\u5173\u95ed\u65f6\u95f4')),
                ('buy_price_rate', models.FloatField(default=1, verbose_name='\u8d2d\u4e70\u8d39\u7387')),
                ('platform_user', models.CharField(max_length=30, verbose_name='\u5e73\u53f0\u8d26\u6237\u7528\u6237\u540d')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modified_datetime', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7cfb\u7edf\u914d\u7f6e\u8868',
                'verbose_name_plural': '\u7cfb\u7edf\u914d\u7f6e\u8868',
            },
        ),
        migrations.CreateModel(
            name='UserBank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bank_name', models.CharField(max_length=255, verbose_name='\u94f6\u884c\u540d')),
                ('bank_account', models.CharField(max_length=255, verbose_name='\u94f6\u884c\u8d26\u53f7')),
                ('tel', models.CharField(max_length=30, null=True, verbose_name='\u7535\u8bdd', blank=True)),
                ('is_enable', models.BooleanField(default=False, verbose_name='\u662f\u5426\u542f\u7528')),
                ('desc', models.CharField(default=b'', max_length=1000, verbose_name='\u5907\u6ce8')),
                ('client_no', models.CharField(default=b'', max_length=100, verbose_name='\u94f6\u884c\u5ba2\u6237\u53f7')),
                ('client_name', models.CharField(default=b'', max_length=100, verbose_name='\u94f6\u884c\u5ba2\u6237\u59d3\u540d')),
                ('is_business_account', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5bf9\u516c\u8d26\u6237')),
                ('is_rescinded', models.BooleanField(default=False, verbose_name='\u662f\u5426\u89e3\u7ea6')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modified_datetime', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('user', models.ForeignKey(related_name='bank_user', verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u94f6\u884c\u5361\u8868',
                'verbose_name_plural': '\u7528\u6237\u94f6\u884c\u5361\u8868',
            },
        ),
    ]
