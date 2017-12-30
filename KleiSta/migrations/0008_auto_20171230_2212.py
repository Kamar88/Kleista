# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0007_auto_20171230_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2017-12-30 22:12'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2017-12-30 22:12'),
        ),
        migrations.AlterField(
            model_name='product',
            name='LSL',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='product',
            name='USL',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='qualityfeature',
            name='Value',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=4),
        ),
    ]
