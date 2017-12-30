# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0008_auto_20171230_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='DateList',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='DateValue1List',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='DateValue2List',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='DecStringOpList',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='DecimalList',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='DecimalOp1List',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='DecimalOp2List',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='DecimalVal1List',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='DecimalVal2List',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='StringDateOplist',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='StringList',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='StringOpList',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactorcriteria',
            name='StringValueList',
        ),
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2017-12-30 23:31'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2017-12-30 23:31'),
        ),
    ]
