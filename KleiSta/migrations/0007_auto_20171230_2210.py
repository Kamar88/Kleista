# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0006_auto_20171230_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2017-12-30 22:10'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2017-12-30 22:10'),
        ),
    ]
