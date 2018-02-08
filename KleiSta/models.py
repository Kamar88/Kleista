from django.db import models
from django.utils import timezone
import datetime

from django.db import transaction

now = datetime.datetime.now()


class Product(models.Model):
    Name = models.CharField(max_length=50)
    ExportDate = models.DateTimeField(
        default=now.strftime("%Y-%m-%d %H:%M"))
    ImportDate = models.DateTimeField(
        default=now.strftime("%Y-%m-%d %H:%M"))
    LSL = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    USL = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    SampleNum = models.IntegerField()
    OrderNum = models.IntegerField()  # to save the order of the data in the excel sheet in case exportDate is not available


class QualityFeature(models.Model):
    Name = models.CharField(max_length=50)
    Value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)


class InfluencingFactor(models.Model):
    Name = models.CharField(max_length=50)
    Value = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)


class Batch(models.Model):
    BatchName = models.CharField(max_length=50)
    BatchDescription = models.CharField(max_length=200)


class BatchProduct(models.Model):
    BatchId = models.ForeignKey(Batch, on_delete=models.CASCADE)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    CreationDate = models.DateTimeField(
        default=timezone.now)



class BatchInfluencingFactorCriteria(models.Model):
    BatchId = models.ForeignKey(Batch, on_delete=models.CASCADE)
    DecimalList = models.TextField()
    DecimalOp1List = models.TextField()
    DecimalOp2List = models.TextField()
    DecimalVal1List = models.TextField()
    DecimalVal2List = models.TextField()
    DecimalBetOp = models.TextField()
    DecStringOpList = models.TextField()
    StringList = models.TextField()
    StringValueList = models.TextField()
    StringOpList = models.TextField()
    StringDateOplist = models.TextField()
    DateList = models.TextField()
    DateValue1List = models.TextField()
    DateValue2List = models.TextField()
    CreationDate = models.DateTimeField(
        default=timezone.now)
    DateOpList = models.TextField()
    Date1OpList = models.TextField()


class Group(models.Model):
    GroupName = models.CharField(max_length=50)
    GroupDescription = models.CharField(max_length=250)
    ExtraFilter = models.BooleanField(default=False)


class GroupBatches(models.Model):
    BatchId = models.ForeignKey(Batch, on_delete=models.CASCADE)
    GroupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    CreationDate = models.DateTimeField(
        default=timezone.now)


class GroupInfluencingFactorCriteria(models.Model):
    GroupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    DecimalList = models.TextField()
    DecimalOp1List = models.TextField()
    DecimalOp2List = models.TextField()
    DecimalVal1List = models.TextField()
    DecimalVal2List = models.TextField()
    DecimalBetOp = models.TextField()
    DecStringOpList = models.TextField()
    StringList = models.TextField()
    StringValueList = models.TextField()
    StringOpList = models.TextField()
    StringDateOplist = models.TextField()
    DateList = models.TextField()
    DateValue1List = models.TextField()
    DateValue2List = models.TextField()
    CreationDate = models.DateTimeField(
        default=timezone.now)
    DateOpList = models.TextField()
    Date1OpList = models.TextField()


class GroupProduct(models.Model):
    GroupId = models.ForeignKey(Group, on_delete=models.CASCADE)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    CreationDate = models.DateTimeField(
        default=timezone.now)
    BatchId= models.ForeignKey(Batch,on_delete=models.CASCADE,default=1)
    QualityFeatureId = models.ForeignKey(QualityFeature, on_delete=models.CASCADE, default=1)
    SampleNo=models.IntegerField(default=1)



