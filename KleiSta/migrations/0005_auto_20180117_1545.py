# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0004_auto_20180114_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupproduct',
            name='QualityFeatureId',
            field=models.ForeignKey(default=1, to='KleiSta.QualityFeature'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2018-01-17 15:45'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2018-01-17 15:45'),
        ),
    ]
