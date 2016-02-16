# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '0002_auto_20160202_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Captcha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipient', models.CharField(unique=True, max_length=32, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('captcha', models.CharField(max_length=15, verbose_name='\u9a8c\u8bc1\u7801')),
                ('deadline_time', models.DateTimeField(null=True, verbose_name='\u8fc7\u671f\u65f6\u95f4', blank=True)),
            ],
            options={
                'verbose_name': '\u9a8c\u8bc1\u7801',
                'verbose_name_plural': '\u9a8c\u8bc1\u7801',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.IntegerField(null=True, verbose_name=b'uid', blank=True)),
                ('username_checked', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xbf\xae\xe6\x94\xb9\xe8\xbf\x87\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('funds_password', models.CharField(max_length=128, null=True, verbose_name='\u8d44\u91d1\u5bc6\u7801', blank=True)),
                ('mobile_phone', models.CharField(unique=True, max_length=15, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('avatar', models.ImageField(upload_to=b'avatar', null=True, verbose_name='\u5934\u50cf', blank=True)),
                ('real_name', models.CharField(default=b'', max_length=127, null=True, verbose_name='\u771f\u5b9e\u59d3\u540d', blank=True)),
                ('cert_type', models.SmallIntegerField(default=0, null=True, verbose_name='\u8bc1\u4ef6\u7c7b\u578b', blank=True, choices=[(0, '\u8eab\u4efd\u8bc1'), (1, '\u7ec4\u7ec7\u673a\u6784\u4ee3\u7801')])),
                ('identification_card_number', models.CharField(max_length=32, null=True, verbose_name='\u8eab\u4efd\u8bc1\u53f7', blank=True)),
                ('identification_card_image_front', models.ImageField(upload_to=b'identification_card', null=True, verbose_name='\u8eab\u4efd\u8bc1\u6b63\u9762\u56fe', blank=True)),
                ('identification_card_image_back', models.ImageField(upload_to=b'identification_card', null=True, verbose_name='\u8eab\u4efd\u8bc1\u80cc\u9762\u56fe', blank=True)),
                ('role', models.CharField(default=b'member', max_length=100, verbose_name='\u89d2\u8272', choices=[(b'member', '\u4f1a\u5458'), (b'ISP', '\u5382\u5546'), (b'dashboard_admin', '\u540e\u53f0\u7ba1\u7406\u5458'), (b'warehouse_staff', '\u4ed3\u5e93\u4eba\u5458'), (b'member_unit', '\u4f1a\u5458\u5355\u4f4d'), (b'trader', '\u4ea4\u6613\u5458')])),
                ('nickname', models.CharField(default=b'', max_length=127, null=True, verbose_name='\u6635\u79f0', blank=True)),
                ('sex', models.PositiveSmallIntegerField(default=3, verbose_name='\u6027\u522b', choices=[(1, '\u7537'), (2, '\u5973'), (3, '\u4fdd\u5bc6')])),
                ('birthday', models.DateField(null=True, blank=True)),
                ('interest', models.CharField(default=b'', max_length=200, null=True, verbose_name='\u5174\u8da3', blank=True)),
                ('address', models.CharField(default=b'', max_length=200, null=True, verbose_name='\u8be6\u7ec6\u5730\u5740', blank=True)),
                ('audit_status', models.PositiveSmallIntegerField(default=0, verbose_name='\u8ba4\u8bc1\u72b6\u6001', choices=[(0, '\u672a\u8ba4\u8bc1'), (1, '\u8ba4\u8bc1\u4e2d'), (2, '\u8ba4\u8bc1\u6210\u529f'), (3, '\u8ba4\u8bc1\u5931\u8d25')])),
                ('pay_pwd', models.CharField(max_length=128, null=True, verbose_name='\u8d44\u91d1\u5bc6\u7801', blank=True)),
                ('pickup_pwd', models.CharField(max_length=128, null=True, verbose_name='\u63d0\u8d27\u5bc6\u7801', blank=True)),
                ('desc', models.CharField(default=b'', max_length=1000, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('introducer', models.CharField(max_length=64, null=True, verbose_name='\u63a8\u8350\u4eba', blank=True)),
                ('register_ip', models.CharField(max_length=64, null=True, verbose_name='\u6ce8\u518cIP', blank=True)),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='\u521b\u5efa\u65e5\u671f', db_index=True)),
                ('created_time', models.TimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='\u4fee\u6539\u65e5\u671f')),
                ('modified_time', models.TimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('region', models.ForeignKey(verbose_name='\u5730\u533a', blank=True, to='address.District', null=True)),
                ('user', models.OneToOneField(verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u989d\u5916\u4fe1\u606f',
                'verbose_name_plural': '\u7528\u6237\u989d\u5916\u4fe1\u606f',
            },
        ),
    ]
