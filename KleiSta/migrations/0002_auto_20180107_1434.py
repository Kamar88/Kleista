# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('KleiSta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupInfluencingFactorCriteria',
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
            ],
        ),
        migrations.CreateModel(
            name='GroupProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CreationDate', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='ExtraFilter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='groupbatches',
            name='CreationDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='product',
            name='ExportDate',
            field=models.DateTimeField(default=b'2018-01-07 14:34'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ImportDate',
            field=models.DateTimeField(default=b'2018-01-07 14:34'),
        ),
        migrations.AddField(
            model_name='groupproduct',
            name='GroupId',
            field=models.ForeignKey(to='KleiSta.Group'),
        ),
        migrations.AddField(
            model_name='groupproduct',
            name='ProductId',
            field=models.ForeignKey(to='KleiSta.Product'),
        ),
        migrations.AddField(
            model_name='groupinfluencingfactorcriteria',
            name='GroupId',
            field=models.ForeignKey(to='KleiSta.Group'),
        ),
    ]
