from django.db import models
from django.utils import timezone


class Product(models.Model):
    Name = models.CharField(max_length=50)
    ExportDate = models.DateTimeField
    ImportDate = models.DateTimeField(
        default=timezone.now)
    LSL = models.DecimalField
    USL = models.DecimalField
    SampleNum = models.IntegerField
    OrderNum = models.IntegerField      #to save the order of the data in the excel sheet in case exportDate is not available


class QualityFeature(models.Model):
    Name = models.CharField(max_length=50)
    Value = models.DecimalField
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
