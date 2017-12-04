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
                ('BatchDescription', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='BatchInfluencingFactor',
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
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50)),
                ('ImportDate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='QualityFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50)),
                ('ProductId', models.ForeignKey(to='KleiSta.Product')),
            ],
        ),
        migrations.AddField(
            model_name='influencingfactor',
            name='ProductId',
            field=models.ForeignKey(to='KleiSta.Product'),
        ),
        migrations.AddField(
            model_name='batchinfluencingfactor',
            name='InflId',
            field=models.ForeignKey(to='KleiSta.InfluencingFactor'),
        ),
    ]
