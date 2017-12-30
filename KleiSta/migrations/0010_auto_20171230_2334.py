# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0009_auto_20171230_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2017-12-30 23:34'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2017-12-30 23:34'),
        ),
    ]
