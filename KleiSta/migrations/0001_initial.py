# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('BatchName', models.CharField(max_length=50)),
                ('BatchDescription', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BatchInfluencingFactorCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DecimalList', models.TextField()),
                ('DecimalOp1List', models.TextField()),
                ('DecimalOp2List', models.TextField()),
                ('DecimalVal1List', models.TextField()),
                ('DecimalVal2List', models.TextField()),
                ('DecimalBetOp', models.TextField()),
                ('DecStringOpList', models.TextField()),
                ('StringList', models.TextField()),
                ('StringValueList', models.TextField()),
                ('StringOpList', models.TextField()),
                ('StringDateOplist', models.TextField()),
                ('DateList', models.TextField()),
                ('DateValue1List', models.TextField()),
                ('DateValue2List', models.TextField()),
                ('CreationDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('DateOpList', models.TextField()),
                ('Date1OpList', models.TextField()),
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
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('GroupName', models.CharField(max_length=50)),
                ('GroupDescription', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='GroupBatches',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('BatchId', models.ForeignKey(to='KleiSta.Batch')),
                ('GroupId', models.ForeignKey(to='KleiSta.Group')),
            ],
        ),
        migrations.CreateModel(
            name='InfluencingFactor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50)),
                ('Value', models.CharField(max_length=50)),
                ('Type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50)),
                ('ExportDate', models.DateTimeField(default=b'2018-01-03 19:36')),
                ('ImportDate', models.DateTimeField(default=b'2018-01-03 19:36')),
                ('LSL', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('USL', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('SampleNum', models.IntegerField()),
                ('OrderNum', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QualityFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50)),
                ('Value', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('ProductId', models.ForeignKey(to='KleiSta.Product')),
            ],
        ),
        migrations.AddField(
            model_name='influencingfactor',
            name='ProductId',
            field=models.ForeignKey(to='KleiSta.Product'),
        ),
        migrations.AddField(
            model_name='batchproduct',
            name='ProductId',
            field=models.ForeignKey(to='KleiSta.Product'),
        ),
    ]
