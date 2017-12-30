# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0005_auto_20171215_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchInfluencingFactorCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DecimalList', models.CharField(max_length=3000)),
                ('DecimalOp1List', models.CharField(max_length=1000)),
                ('DecimalOp2List', models.CharField(max_length=1000)),
                ('DecimalVal1List', models.CharField(max_length=3000)),
                ('DecimalVal2List', models.CharField(max_length=3000)),
                ('DecStringOpList', models.CharField(max_length=1000)),
                ('StringList', models.CharField(max_length=3000)),
                ('StringValueList', models.CharField(max_length=3000)),
                ('StringOpList', models.CharField(max_length=3000)),
                ('StringDateOplist', models.CharField(max_length=3000)),
                ('DateList', models.CharField(max_length=3000)),
                ('DateValue1List', models.CharField(max_length=3000)),
                ('DateValue2List', models.CharField(max_length=3000)),
                ('CreationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('BatchId', models.ForeignKey(to='KleiSta.Batch')),
            ],
        ),
        migrations.CreateModel(
            name='BatchProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CreationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('BatchId', models.ForeignKey(to='KleiSta.Batch')),
            ],
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactor',
            name='BatchId',
        ),
        migrations.RemoveField(
            model_name='batchinfluencingfactor',
            name='InflId',
        ),
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2017-12-30 22:04'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2017-12-30 22:04'),
        ),
        migrations.AlterField(
            model_name='product',
            name='LSL',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='USL',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='qualityfeature',
            name='Value',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
        ),
        migrations.DeleteModel(
            name='BatchInfluencingFactor',
        ),
        migrations.AddField(
            model_name='batchproduct',
            name='ProductId',
            field=models.ForeignKey(to='KleiSta.Product'),
        ),
    ]
