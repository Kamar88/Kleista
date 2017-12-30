# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0010_auto_20171230_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='BatchDescription',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2017-12-30 23:35'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2017-12-30 23:35'),
        ),
    ]
