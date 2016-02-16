# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import oscar.core.validators
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0002_auto_20150217_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u540d\u5b57')),
            ],
            options={
                'verbose_name': '\u4ea7\u54c1\u7ec4',
                'verbose_name_plural': '\u4ea7\u54c1\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='SearchFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_value', models.CharField(help_text='\u533a\u95f4\u503c\u8bbe\u7f6e\u6210 eg:30\u5ea6-40\u5ea6', max_length=120, null=True, verbose_name='\u641c\u7d22\u503c', blank=True)),
                ('value_range', models.CharField(choices=[(b'>', '\u4ee5\u4e0a'), (b'<', '\u4ee5\u4e0b')], max_length=120, blank=True, help_text='\u4e0d\u662f\u8303\u56f4\u7684\u5c5e\u6027\u503c\u4e3a\u7a7a', null=True, verbose_name='\u9009\u62e9\u8303\u56f4')),
                ('search_order', models.IntegerField(null=True, verbose_name='\u641c\u7d22\u503c\u6392\u5217\u987a\u5e8f', blank=True)),
                ('chose', models.BooleanField(default=True, verbose_name='\u9009\u62e9\u8be5\u641c\u7d22\u503c')),
            ],
            options={
                'ordering': ['attribute'],
                'verbose_name': '\u641c\u7d22\u5c5e\u6027\u914d\u7f6e',
                'verbose_name_plural': '\u641c\u7d22\u5c5e\u6027\u914d\u7f6e',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='product_class',
            field=models.ForeignKey(related_name='categories', blank=True, to='catalogue.ProductClass', help_text='\u9009\u62e9\u5206\u7c7b\u7684\u7c7b\u5c5e\u6027\uff0c\u7ed1\u5b9a\u5206\u7c7b\u5546\u54c1\u5c5e\u6027\u503c', null=True, verbose_name='\u5206\u7c7b\u7c7b\u5c5e\u6027'),
        ),
        migrations.AddField(
            model_name='product',
            name='browse_num',
            field=models.BigIntegerField(default=0, verbose_name='\u6d4f\u89c8\u6b21\u6570'),
        ),
        migrations.AddField(
            model_name='product',
            name='featured_hot',
            field=models.BooleanField(default=False, verbose_name='\u4e3b\u63a8\u70ed\u5356'),
        ),
        migrations.AddField(
            model_name='product',
            name='hot_deals',
            field=models.BooleanField(default=False, verbose_name='\u706b\u70ed\u4fc3\u9500'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_associate',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5173\u8054'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_on_shelves',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u4e0a\u67b6'),
        ),
        migrations.AddField(
            model_name='product',
            name='new_listing',
            field=models.BooleanField(default=False, verbose_name='\u65b0\u54c1\u4e0a\u5e02'),
        ),
        migrations.AddField(
            model_name='product',
            name='opening_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='\u4e0a\u5e02\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_long_image',
            field=models.ImageField(upload_to=b'images/products/%Y/%m/', null=True, verbose_name='\u5e7f\u544a\u957f\u56fe', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='selection_reputation',
            field=models.BooleanField(default=False, verbose_name='\u53e3\u7891\u7504\u9009'),
        ),
        migrations.AddField(
            model_name='product',
            name='trader',
            field=models.ForeignKey(related_name='trader', verbose_name='\u4ea4\u6613\u5458', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='index',
            field=models.IntegerField(null=True, verbose_name='\u6392\u5e8f', blank=True),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='search_filter',
            field=models.BooleanField(default=True, help_text='\u8bbe\u7f6e\u4e0d\u9700\u8981\u641c\u7d22\u7684\u5c5e\u6027\u503c', verbose_name='\u662f\u5426\u641c\u7d22'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(related_name='products', on_delete=django.db.models.deletion.PROTECT, blank=True, to='catalogue.ProductClass', help_text='Choose what type of product this is', null=True, verbose_name='Product type'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='code',
            field=models.SlugField(max_length=128, verbose_name='Code', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z_][0-9a-zA-Z_]*$', message="Code can only contain the letters a-z, A-Z, digits, and underscores, and can't start with a digit"), oscar.core.validators.non_python_keyword]),
        ),
        migrations.AddField(
            model_name='searchfilter',
            name='attribute',
            field=models.ForeignKey(verbose_name='Attribute', to='catalogue.ProductAttribute'),
        ),
        migrations.AddField(
            model_name='productgroup',
            name='attr',
            field=models.ManyToManyField(related_name='product_group_attr', verbose_name='\u4ea7\u54c1\u7ec4\u5c5e\u6027', to='catalogue.ProductAttribute', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_group',
            field=models.ForeignKey(related_name='product_group', verbose_name='\u4ea7\u54c1\u7ec4', blank=True, to='catalogue.ProductGroup', null=True),
        ),
    ]
