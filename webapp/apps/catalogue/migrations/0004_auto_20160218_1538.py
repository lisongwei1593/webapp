# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20160202_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productgroup',
            name='attr',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_group',
        ),
        migrations.DeleteModel(
            name='ProductGroup',
        ),
    ]
