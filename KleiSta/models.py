from django.db import models
from django.utils import timezone
import datetime

now = datetime.datetime.now()


class Product(models.Model):
    Name = models.CharField(max_length=50)
    ExportDate = models.DateTimeField(
        default=now.strftime("%Y-%m-%d %H:%M"))
    ImportDate = models.DateTimeField(
        default=now.strftime("%Y-%m-%d %H:%M"))
    LSL = models.DecimalField(max_digits=5, decimal_places=2,default=0.0)
    USL = models.DecimalField(max_digits=5, decimal_places=2,default=0.0)
    SampleNum = models.IntegerField()
    OrderNum = models.IntegerField()  # to save the order of the data in the excel sheet in case exportDate is not available


class QualityFeature(models.Model):
    Name = models.CharField(max_length=50)
    Value = models.DecimalField(max_digits=5, decimal_places=2,default=0.0)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)


class InfluencingFactor(models.Model):
    Name = models.CharField(max_length=50)
    Value = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)


class Batch(models.Model):
    BatchName = models.CharField(max_length=50)
    BatchDescription = models.CharField(max_length=250)


class BatchInfluencingFactor(models.Model):
    BatchId = models.ForeignKey(Batch, on_delete=models.CASCADE)
    InflId = models.ForeignKey(InfluencingFactor, on_delete=models.CASCADE)
    CreationDate = models.DateTimeField(
        default=timezone.now)


class Group(models.Model):
    GroupName = models.CharField(max_length=50)
    GroupDescription = models.CharField(max_length=250)


class GroupBatches(models.Model):
    BatchId = models.ForeignKey(Batch, on_delete=models.CASCADE)
    GroupId = models.ForeignKey(Group, on_delete=models.CASCADE)
