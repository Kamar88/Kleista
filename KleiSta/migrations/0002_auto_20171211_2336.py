# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AddField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2017-12-11 23:36'),
        ),
        migrations.AddField(
            model_name='product',
            name='LSL',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='product',
            name='USL',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='qualityfeature',
            name='Value',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2017-12-11 23:36'),
        ),
    ]
