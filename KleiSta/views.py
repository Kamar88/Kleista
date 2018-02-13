from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import xlrd  # use this library to extract the data from the excel sheet
# for documentation check https://pypi.python.org/pypi/xlrd
from models import GroupProduct, Product, InfluencingFactor, QualityFeature, Group, Batch, BatchProduct, GroupBatches, \
    BatchInfluencingFactorCriteria, GroupInfluencingFactorCriteria
from django.db.models import *
from decimal import *
# use Django ORM to optimize query and save to database
from django.db.models import Q
# use bulk save to be able to save huge amount of the data
# with the minimum time
from django_bulk_update.helper import bulk_update
from django.conf import settings
import datetime
from django.views.generic import TemplateView
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
import plotly.offline as opy
import plotly.graph_objs as go
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import norm


def home(request):
    if request.method == 'POST' and 'reset' in request.POST:
        # if the user want to reset the setup data, clear all the database object
        Product.objects.all().delete()
        InfluencingFactor.objects.all().delete()
        QualityFeature.objects.all().delete()
        Group.objects.all().delete()
        Batch.objects.all().delete()
        BatchProduct.objects.all().delete()
        GroupBatches.objects.all().delete()
        GroupProduct.objects.all().delete()
        GroupInfluencingFactorCriteria.objects.all().delete()
        BatchInfluencingFactorCriteria.objects.all().delete()
    elif (request.method == 'POST' and 'DataTable' in request.POST) or (
                    request.method == 'POST' and 'SubmitList' in request.POST):
        # if the user submit the datatable excel sheet or the user wants to set the set up configuaration
        # if the database is not empty, Clear the data base first
        productc = Product.objects.all().count()
        if productc > 0:
            Product.objects.all().delete()
            InfluencingFactor.objects.all().delete()
            QualityFeature.objects.all().delete()
            Group.objects.all().delete()
            Batch.objects.all().delete()
            BatchProduct.objects.all().delete()
            GroupBatches.objects.all().delete()
        if request.method == 'POST' and 'DataTable' in request.POST:
            # if the user wants to upload the excelsheet
            # process the datamanually
            myfile = request.FILES['DataTableF']  # get the file from the post request
            fs = FileSystemStorage()  # save the file in the server
            filename = fs.save(myfile.name,
                               myfile)  # get the name of the file in case message should be displayed to user
            uploaded_file_url = fs.url(filename)
            # open the document that the user has upload to the database
            book = xlrd.open_workbook(settings.MEDIA_ROOT + "\\" + filename)
            # if the excel sheet is not empty,process data otherwise display error message
            xl_sheet = book.sheet_by_index(0)
            if xl_sheet.nrows > 0:
                row = xl_sheet.row(0)  # get the first row in the excelsheet which has the column name
                col_list = []
                # get the list of the column name and send the databack to the template
                # send also the name of the file that user uploaded, so you can process later
                for cnt in range(len(row)): col_list.append(row[cnt].value.encode('utf-8').strip())
                return render(request, 'Setup.html', {'ColList': col_list, 'File_Name': filename})
            else:
                uploaded_file_url = "The Data Table that you have uploaded is empty. Please Upload another Data Table"
                return render(request, 'Setup.html', {'uploaded_file_url': uploaded_file_url})
        elif request.method == 'POST' and 'SubmitList' in request.POST:
            # if the user categorized the data and it submitted the list to the server,
            # process the data manually

            # get the data from the post manually
            productn = request.POST.getlist('ProductName')
            LSL = request.POST.getlist('LSL')
            USL = request.POST.getlist('USL')
            INF = request.POST.getlist('InflFactor')
            QF = request.POST.getlist('QFeature')
            filename = request.POST.get('FileName')
            Date = request.POST.getlist('Date')

            book = xlrd.open_workbook(settings.MEDIA_ROOT + "\\" + filename.encode('utf-8').strip())
            xl_sheet = book.sheet_by_index(0)

            infListS = []  # create list to save the influencing factors temproray in it then do bulk save
            qfList = []  # create list to save the quality features temproray in it then do bulk save

            # loop through the columns in the excel sheet and process the data
            # Start from row 1 while row o is alread saved to database to set the setup data
            # when extracting the data from the excel sheet the data can fall in one of 3 categories
            # type 1 = string, 2=Decimal, 3=Date.
            # the used method in xlrd are xl_sheet.nrows which returns the number of rows in excelsheet
            #
            for row in range(1, xl_sheet.nrows):
                # create product object to save data to database
                product = Product()
                # Product details
                product.Name = xl_sheet.cell_value(row, int(productn[0])).encode('utf-8').strip()
                # cell = xl_sheet.cell_value(row, int(productn[0])).encode('utf-8').strip()
                product.OrderNum = row
                product.SampleNum = 0
                # type = xl_sheet.cell_type(row, int(productn[0]))
                if len(LSL):
                    type = xl_sheet.cell_type(row, int(LSL[0]))
                    if (type == 2):
                        product.LSL = Decimal(str(xl_sheet.cell_value(row, int(LSL[0]))).encode('utf-8'))
                    else:
                        product.LSL = 0
                else:
                    product.LSL = 0
                if len(USL):
                    type = xl_sheet.cell_type(row, int(USL[0]))
                    if (type == 2):
                        product.USL = Decimal(str(xl_sheet.cell_value(row, int(USL[0]))).encode('utf-8'))
                    else:
                        product.USL = 0
                else:
                    product.USL = 0
                if len(Date):
                    date1 = xl_sheet.cell_value(row, int(Date[0]))
                    product.ExportDate = datetime.datetime(
                        *xlrd.xldate_as_tuple(xl_sheet.cell_value(row, int(Date[0])), book.datemode))
                else:
                    product.ExportDate = " "
                # save the product, so you can use the product id to save the Influencing factor and quality features
                product.save()
                # QualityFeatures
                for QFI in QF:
                    # create an instance of the quality features
                    # quality features should be always of type 2 decimal.
                    qfc = QualityFeature()
                    qfc.Name = xl_sheet.cell_value(0, int(QFI)).encode('utf-8').strip()
                    type = xl_sheet.cell_type(row, int(QFI))
                    if (type == 2):
                        qfc.Value = Decimal(str(xl_sheet.cell_value(row, int(QFI))).encode('utf-8'))
                    else:
                        qfc.Value = 0
                    qfc.ProductId = product
                    qfList.append(qfc)
                    # Influncing Factor Details
                for IFE in INF:
                    ifc = InfluencingFactor()
                    ifc.Name = xl_sheet.cell_value(0, int(IFE)).encode('utf-8').strip()
                    type = xl_sheet.cell_type(row, int(IFE))
                    if (type == 2):
                        ifc.Type = "Decimal"
                        ifc.Value = Decimal(str(xl_sheet.cell_value(row, int(IFE))).encode('utf-8'))
                    elif (type == 1):
                        ifc.Type = "String"
                        ifc.Value = xl_sheet.cell_value(row, int(IFE)).encode('utf-8').strip()
                    elif (type == 3):
                        ifc.Type = "Date"
                        ifc.Value = datetime.datetime(
                            *xlrd.xldate_as_tuple(xl_sheet.cell_value(row, int(IFE)), book.datemode))
                    else:
                        ifc.Value = 0
                    ifc.ProductId = product
                    # ifc.save()
                    infListS.append(ifc)
                if len(Date):
                    ifc = InfluencingFactor()
                    ifc.Name = xl_sheet.cell_value(0, int(Date[0])).encode('utf-8').strip()
                    ifc.Type = "Date"
                    ifc.ProductId = product
                    ifc.Value = datetime.datetime(
                        *xlrd.xldate_as_tuple(xl_sheet.cell_value(row, int(Date[0])), book.datemode))
                    # ifc.save()
                    infListS.append(ifc)
            # do bulk save for quality feature and influencing factors
            InfluencingFactor.objects.bulk_create(infListS)
            QualityFeature.objects.bulk_create(qfList)

            # after saving the data count the number of samples for each product
            # save it to the database using loop and bulk update

            difPro = Product.objects.values('Name').distinct()

            productList = []
            for p in difPro:
                product = Product.objects.filter(Name=p['Name'])
                count = 1
                for ip in product:
                    ip.SampleNum = count
                    count = count + 1
                    productList.append(ip)

            bulk_update(productList, update_fields=['SampleNum'])

    return render(request, 'Setup.html', {})


def batch(request):
    if request.method == 'POST' and 'SubmitBatchDetail' in request.POST:
        # BatchInformation
        BatchN = request.POST.get('BatchName')
        BatchD = request.POST.get('BatchDescription')
        # DecimalList retriving
        listinfDe = request.POST.getlist('InfDe')  # retrive all the decimal list names from the batch page
        Decimalval1 = request.POST.getlist(
            'DecimalValueInf1')  # retrive all the decimal list value1 from the batch page
        Decimalval2 = request.POST.getlist(
            'DecimalValueInf2')  # retrive all the decimal list value1 from the batch page
        operationDe = request.POST.getlist('OperationDec')  # retrive the operation between the decimal values
        operationBt1 = request.POST.getlist('OprBetween1')  # operation for the first decimal value lessThan and so on
        operationBt2 = request.POST.getlist('OprBetween2')  # operation for the second decimal value lessThan and so on

        # Datelist retriving
        listinfDa = request.POST.getlist('InfDa')  # retrive all the date list names from the batch page
        listdate1 = request.POST.getlist('Date1')  # retrive all the date1 list value from the batch page
        listdate2 = request.POST.getlist('Date2')  # retrive all the date2 list value from the batch page
        operationDate = request.POST.getlist('OperationDat')  # retrive the operation between the date values
        OperationDate1 = request.POST.getlist('OperationDate1')
        # StringList retriving
        listinfS = request.POST.getlist('InfS')  # retrive all the string lists from the batch page
        listinfSV = request.POST.getlist(
            'InfluencingFactorSV')  # retrive all the string value lists from the batch page
        operationS = request.POST.getlist('OperationS')  # retrive the operation between the String values

        operationDeS = request.POST.getlist(
            'OperationDecString')  # get the operation between decimal Lists and String Lists
        operationSD = request.POST.getlist(
            'OperationStringDate')  # get the operation between String Lists and date list

        # convert the decimal influencing factor from unicode to normal string
        infoDecEncoded = [x.encode('UTF8') for x in listinfDe]
        infoDecValue1Encoded = [x.encode('UTF8') for x in Decimalval1]
        infoDecValue2Encoded = [x.encode('UTF8') for x in Decimalval2]
        infoDecOpBetwEncoded = [x.encode('UTF8') for x in operationDe]
        infoDecOpVal1wEncoded = [x.encode('UTF8') for x in operationBt1]
        infoDecOpVal2wEncoded = [x.encode('UTF8') for x in operationBt2]

        # retrive all the influencing factors that the user specify in the decimal list
        infODec = InfluencingFactor.objects.filter(Name__in=infoDecEncoded)
        InfDecListID = [];
        infDecListCID = [];

        cd = 0;
        for i in infoDecEncoded:
            qn = Q(Name=i)
            qv1 = Q()
            qv2 = Q()
            if (infoDecValue1Encoded[cd]):
                if (infoDecOpVal1wEncoded[cd] == 'lessThan'):
                    qv1 = Q(Value__lt=(infoDecValue1Encoded[cd]))
                elif (infoDecOpVal1wEncoded[cd] == 'lessThanEqual'):
                    qv1 = Q(Value__lte=(infoDecValue1Encoded[cd]))
                elif (infoDecOpVal1wEncoded[cd] == 'greater'):
                    qv1 = Q(Value__gt=(infoDecValue1Encoded[cd]))
                elif (infoDecOpVal1wEncoded[cd] == 'greaterThanEqual'):
                    qv1 = Q(Value__gte=(infoDecValue1Encoded[cd]))
                elif (infoDecOpVal1wEncoded[cd] == 'Equal'):
                    qv1 = Q(Value=(infoDecValue1Encoded[cd]))
            if (infoDecValue2Encoded[cd]):
                if (infoDecOpVal2wEncoded[cd] == 'lessThan'):
                    qv2 = Q(Value__lt=(infoDecValue2Encoded[cd]))
                elif (infoDecOpVal2wEncoded[cd] == 'lessThanEqual'):
                    qv2 = Q(Value__lte=(infoDecValue2Encoded[cd]))
                elif (infoDecOpVal2wEncoded[cd] == 'greater'):
                    qv2 = Q(Value__gt=(infoDecValue2Encoded[cd]))
                elif (infoDecOpVal2wEncoded[cd] == 'greaterThanEqual'):
                    qv2 = Q(Value__gte=(infoDecValue2Encoded[cd]))
                elif (infoDecOpVal2wEncoded[cd] == 'Equal'):
                    qv2 = Q(Value=(infoDecValue2Encoded[cd]))
            qi = (qn & qv1 & qv2)  # build the clause of the query depending on the previous selected value
            if (cd > 0):
                if (infoDecOpBetwEncoded[cd] == 'And'):
                    q2 = InfluencingFactor.objects.filter(qi).values(
                        'ProductId_id').distinct()  # get the current query result depending on the current previous condition
                    qdecimal = qdecimal.filter(ProductId_id__in=q2)  # save the final query result of decimal list
                    # q = q & qi
                elif (infoDecOpBetwEncoded[cd] == 'Or'):
                    q2 = InfluencingFactor.objects.filter(qi).values('ProductId_id').distinct()
                    qdecimal = qdecimal | q2
                    # q = q | qi
            else:
                qdecimal = InfluencingFactor.objects.filter(qi).values('ProductId_id').distinct()
                # q= q & qi

            cd = cd + 1

        # create the query result of the string list
        # Encode the string lists
        InfoStrEncoded = [x.encode('UTF8') for x in listinfS]  # It includes the string influencing factor names
        InfoStrValEncoded = [x.encode('UTF8') for x in
                             listinfSV]  # It includes the string influencing factor names with its value
        InfoStrOpEncoded = [x.encode('UTF8') for x in operationS]  # It includes the operation between the string value

        qString = Q()
        cs = 0;

        # two loops to link the name of the string with its values and filter the influencing factor table.
        for name in InfoStrEncoded:
            qName = Q(Name=name)  # build the filter criteria of the query by sitting the name first of all
            StrValue = []
            for s in InfoStrValEncoded:  # checks all the value of the string name and append it is vale to list
                if (name == s.split(':')[1]):
                    StrValue.append(s.split(':')[0])
            # filter the value accroding to string Name and the list of the value for this name
            qStringInside = InfluencingFactor.objects.filter(qName, Value__in=StrValue).values(
                'ProductId_id').distinct()

            # combine the string list values and filter the data according to that
            if (cs > 0):
                if (InfoStrOpEncoded[cs] == 'And'):
                    qString = qString.filter(ProductId_id__in=qStringInside)
                else:
                    qString = qString | qStringInside
            else:
                qString = qStringInside  # if the string list include only one item or first time intialization
            cs = cs + 1  # to access the correct index of the operation between strings list

        # create the result of the date list
        # encode the date lists
        InfoValDate1Encoded = [x.encode('UTF8') for x in listdate1]
        InfoValDate2Encoded = [x.encode('UTF8') for x in listdate2]
        InfoDateEncoded = [x.encode('UTF8') for x in listinfDa]
        InfoDateOpEncoded = [x.encode('UTF8') for x in operationDate]
        InfoDate1OpEncoded = [x.encode('UTF8') for x in OperationDate1]

        cda = 0;
        qDateInside = Q()
        for date in InfoDateEncoded:
            qn = Q(Name=date)
            qSD = InfoValDate1Encoded[cda]
            qED = InfoValDate2Encoded[cda]
            if (qSD and qED):
                qDateInside = InfluencingFactor.objects.filter(qn, Value__range=(qSD, qED)).values(
                    'ProductId_id').distinct()
            elif qSD:
                if (InfoDate1OpEncoded[cda] == 'lessThan'):
                    qv1 = Q(Value__lt=(InfoValDate1Encoded[cda]))
                    qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                elif (InfoDate1OpEncoded[cda] == 'lessThanEqual'):
                    qv1 = Q(Value__lte=(InfoValDate1Encoded[cda]))
                    qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                elif (InfoDate1OpEncoded[cda] == 'greater'):
                    qv1 = Q(Value__gt=(InfoValDate1Encoded[cda]))
                    qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                elif (InfoDate1OpEncoded[cda] == 'greaterThanEqual'):
                    qv1 = Q(Value__gte=(InfoValDate1Encoded[cda]))
                    qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                elif (InfoDate1OpEncoded[cda] == 'Equal'):
                    qv1 = Q(Value=(InfoValDate1Encoded[cda]))
                    qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                else:
                    qDateInside = InfluencingFactor.objects.filter(qn, Value=qSD).values('ProductId_id').distinct()
            if (cda > 0):
                if (InfoDateOpEncoded[cda] == 'And'):
                    qDate = qDate.filter(ProductId_id__in=qDateInside)
                else:
                    qDate = qDate | qDateInside
            else:
                qDate = qDateInside  # if the string list include only one item or first time intialization
                cda = cda + 1  # to access the c

        OperationDeSEncode = [x.encode('UTF8') for x in operationDeS]
        operationSDEncode = [x.encode('UTF8') for x in operationSD]

        QBatch = Q()
        if (OperationDeSEncode[0] == 'Or' and qString):
            QBatch = qdecimal | qString
        else:
            if (qdecimal and qString):
                QBatch = qdecimal.filter(ProductId_id__in=qString)
            elif qdecimal:
                QBatch = qdecimal
            else:
                QBatch = qString

        if (operationSDEncode[0] == 'Or' and qDate):
            QBatch = QBatch | qDate
        else:
            if (QBatch and qDate):
                QBatch = QBatch.filter(ProductId_id__in=qDate)
            elif QBatch:
                QBatch = QBatch
            else:
                QBatch = qDate

        QBatchProduct = Product.objects.filter(id__in=QBatch)

        # save Batch details to database
        batch = Batch()
        batch.BatchName = BatchN
        batch.BatchDescription = BatchD
        batch.save()

        # save batch details with influencing factor to batchinfluencingFactortable
        batchCriteria = BatchInfluencingFactorCriteria()
        batchCriteria.BatchId = batch
        batchCriteria.DateList = InfoDateEncoded
        batchCriteria.DateValue1List = InfoValDate1Encoded
        batchCriteria.DateValue2List = InfoValDate2Encoded
        batchCriteria.DateOpList = InfoDateOpEncoded
        batchCriteria.Date1OpList = InfoDate1OpEncoded
        batchCriteria.StringDateOplist = operationSDEncode
        batchCriteria.StringList = InfoStrEncoded
        batchCriteria.StringOpList = InfoStrOpEncoded
        batchCriteria.StringValueList = InfoStrValEncoded
        batchCriteria.DecStringOpList = OperationDeSEncode
        batchCriteria.DecimalList = infoDecEncoded
        batchCriteria.DecimalOp1List = infoDecOpVal1wEncoded
        batchCriteria.DecimalOp2List = infoDecOpVal2wEncoded
        batchCriteria.DecimalVal1List = infoDecValue1Encoded
        batchCriteria.DecimalVal2List = infoDecValue2Encoded
        batchCriteria.DecimalBetOp = infoDecOpBetwEncoded
        batchCriteria.save()

        batchProductList = []
        # save the batch with the product that belong to it
        for p in QBatchProduct:
            batchProduct = BatchProduct()
            batchProduct.BatchId = batch
            batchProduct.ProductId = p
            batchProductList.append(batchProduct)
            # batchProduct.save()
        BatchProduct.objects.bulk_create(batchProductList)
        infVList = InfluencingFactor.objects.filter(ProductId__in=QBatchProduct.values('id').distinct())
        return render(request, 'CreatedBatchDetails.html',
                      {'QBatchProduct': QBatchProduct.distinct(), 'batch': batch, 'infVLisL': infVList})
        # return render(request,'group.html' ,{})
    else:

        infLD = InfluencingFactor.objects.filter(Type="Decimal").values('Name').order_by('Name').distinct()
        infLS = InfluencingFactor.objects.filter(Type="String").values('Name').order_by('Name').distinct()
        infSV = InfluencingFactor.objects.filter(Type="String").values('Name', 'Value').order_by('Name',
                                                                                                 'Value').distinct()
        infLDT = InfluencingFactor.objects.filter(Type="Date").values('Name').order_by('Name').distinct()

        return render(request, 'Batch.html', {'infLD': infLD, 'infLS': infLS, 'infLDT': infLDT, 'infSV': infSV})


def CreatedBatchDetails(request):
    return render(request, "CreatedBatchDetails.html", {})


def group(request):
    if request.method == 'POST' and 'SubmitGroupDetail' in request.POST:

        # get group data and save them to database
        group = Group()
        groupN = request.POST.get('GroupName')
        groupD = request.POST.get('GroupDescription')
        qFeature = request.POST.get('QFeatureS')
        group.GroupName = groupN
        group.GroupDescription = groupD
        if request.POST.get('InfCb') == '1':
            group.ExtraFilter = True;
        else:
            group.ExtraFilter = False;
        group.save()

        # getBatches that are related to group
        groupBatches = request.POST.getlist('SBatches')

        # retrive the batch with the product that belong to it with the quality features
        ProductInBatches1 = BatchProduct.objects.filter(BatchId_id__in=groupBatches,
                                                        ProductId__qualityfeature__Name=qFeature) \
            .values('BatchId__BatchDescription', 'BatchId__BatchName', 'BatchId_id',
                    'ProductId__Name', 'ProductId__ExportDate', 'ProductId__LSL', 'ProductId__USL',
                    'ProductId__SampleNum',
                    'ProductId__OrderNum', 'ProductId__qualityfeature__Name', 'ProductId__qualityfeature__Value',
                    'ProductId__qualityfeature__id')
        ProductInBatches = BatchProduct.objects.filter(BatchId_id__in=groupBatches,
                                                       ProductId__qualityfeature__Name=qFeature) \
            .values('id', 'BatchId__BatchDescription', 'BatchId__BatchName', 'BatchId_id',
                    'ProductId__Name', 'ProductId__ExportDate', 'ProductId__LSL', 'ProductId__USL',
                    'ProductId__qualityfeature__Name', 'ProductId__qualityfeature__Value',
                    'ProductId__qualityfeature__Value')

        ProductInBatchesC = ProductInBatches.values('BatchId_id', 'ProductId__Name').order_by('BatchId_id',
                                                                                              'ProductId__Name').annotate(
            total=Count('ProductId__Name'))

        # save Batches with their group to database
        BatchList = []
        for B in groupBatches:
            groupBatch = GroupBatches()
            groupBatch.GroupId = group
            groupBatch.BatchId_id = B
            BatchList.append(groupBatch)
        GroupBatches.objects.bulk_create(BatchList)

        # if the group has more filter then get these filter and save the data to group product data
        if request.POST.get('InfCb') == '1':
            # DecimalList retriving
            listinfDe = request.POST.getlist('InfDe')  # retrive all the decimal list names from the batch page
            Decimalval1 = request.POST.getlist(
                'DecimalValueInf1')  # retrive all the decimal list value1 from the batch page
            Decimalval2 = request.POST.getlist(
                'DecimalValueInf2')  # retrive all the decimal list value1 from the batch page
            operationDe = request.POST.getlist('OperationDec')  # retrive the operation between the decimal values
            operationBt1 = request.POST.getlist(
                'OprBetween1')  # operation for the first decimal value lessThan and so on
            operationBt2 = request.POST.getlist(
                'OprBetween2')  # operation for the second decimal value lessThan and so on

            # Datelist retriving
            listinfDa = request.POST.getlist('InfDa')  # retrive all the date list names from the batch page
            listdate1 = request.POST.getlist('Date1')  # retrive all the date1 list value from the batch page
            listdate2 = request.POST.getlist('Date2')  # retrive all the date2 list value from the batch page
            operationDate = request.POST.getlist('OperationDat')  # retrive the operation between the date values
            OperationDate1 = request.POST.getlist('OperationDate1')
            # StringList retriving
            listinfS = request.POST.getlist('InfS')  # retrive all the string lists from the batch page
            listinfSV = request.POST.getlist(
                'InfluencingFactorSV')  # retrive all the string value lists from the batch page
            operationS = request.POST.getlist('OperationS')  # retrive the operation between the String values

            operationDeS = request.POST.getlist(
                'OperationDecString')  # get the operation between decimal Lists and String Lists
            operationSD = request.POST.getlist(
                'OperationStringDate')  # get the operation between String Lists and date list

            # convert the decimal influencing factor from unicode to normal string
            infoDecEncoded = [x.encode('UTF8') for x in listinfDe]
            infoDecValue1Encoded = [x.encode('UTF8') for x in Decimalval1]
            infoDecValue2Encoded = [x.encode('UTF8') for x in Decimalval2]
            infoDecOpBetwEncoded = [x.encode('UTF8') for x in operationDe]
            infoDecOpVal1wEncoded = [x.encode('UTF8') for x in operationBt1]
            infoDecOpVal2wEncoded = [x.encode('UTF8') for x in operationBt2]

            # retrive all the influencing factors that the user specify in the decimal list
            infODec = InfluencingFactor.objects.filter(Name__in=infoDecEncoded)
            InfDecListID = [];
            infDecListCID = [];

            cd = 0;
            for i in infoDecEncoded:
                qn = Q(Name=i)
                qv1 = Q()
                qv2 = Q()
                if (infoDecValue1Encoded[cd]):
                    if (infoDecOpVal1wEncoded[cd] == 'lessThan'):
                        qv1 = Q(Value__lt=(infoDecValue1Encoded[cd]))
                    elif (infoDecOpVal1wEncoded[cd] == 'lessThanEqual'):
                        qv1 = Q(Value__lte=(infoDecValue1Encoded[cd]))
                    elif (infoDecOpVal1wEncoded[cd] == 'greater'):
                        qv1 = Q(Value__gt=(infoDecValue1Encoded[cd]))
                    elif (infoDecOpVal1wEncoded[cd] == 'greaterThanEqual'):
                        qv1 = Q(Value__gte=(infoDecValue1Encoded[cd]))
                    elif (infoDecOpVal1wEncoded[cd] == 'Equal'):
                        qv1 = Q(Value=(infoDecValue1Encoded[cd]))
                if (infoDecValue2Encoded[cd]):
                    if (infoDecOpVal2wEncoded[cd] == 'lessThan'):
                        qv2 = Q(Value__lt=(infoDecValue2Encoded[cd]))
                    elif (infoDecOpVal2wEncoded[cd] == 'lessThanEqual'):
                        qv2 = Q(Value__lte=(infoDecValue2Encoded[cd]))
                    elif (infoDecOpVal2wEncoded[cd] == 'greater'):
                        qv2 = Q(Value__gt=(infoDecValue2Encoded[cd]))
                    elif (infoDecOpVal2wEncoded[cd] == 'greaterThanEqual'):
                        qv2 = Q(Value__gte=(infoDecValue2Encoded[cd]))
                    elif (infoDecOpVal2wEncoded[cd] == 'Equal'):
                        qv2 = Q(Value=(infoDecValue2Encoded[cd]))
                qi = (qn & qv1 & qv2)  # build the clause of the query depending on the previous selected value
                if (cd > 0):
                    if (infoDecOpBetwEncoded[cd] == 'And'):
                        q2 = InfluencingFactor.objects.filter(qi).values(
                            'ProductId_id').distinct()  # get the current query result depending on the current previous condition
                        qdecimal = qdecimal.filter(ProductId_id__in=q2)  # save the final query result of decimal list
                        # q = q & qi
                    elif (infoDecOpBetwEncoded[cd] == 'Or'):
                        q2 = InfluencingFactor.objects.filter(qi).values('ProductId_id').distinct()
                        qdecimal = qdecimal | q2
                        # q = q | qi
                else:
                    qdecimal = InfluencingFactor.objects.filter(qi).values('ProductId_id').distinct()
                    # q= q & qi

                cd = cd + 1

            # create the query result of the string list
            # Encode the string lists
            InfoStrEncoded = [x.encode('UTF8') for x in listinfS]  # It includes the string influencing factor names
            InfoStrValEncoded = [x.encode('UTF8') for x in
                                 listinfSV]  # It includes the string influencing factor names with its value
            InfoStrOpEncoded = [x.encode('UTF8') for x in
                                operationS]  # It includes the operation between the string value

            qString = Q()
            cs = 0;

            # two loops to link the name of the string with its values and filter the influencing factor table.
            for name in InfoStrEncoded:
                qName = Q(Name=name)  # build the filter criteria of the query by sitting the name first of all
                StrValue = []
                for s in InfoStrValEncoded:  # checks all the value of the string name and append it is vale to list
                    if (name == s.split(':')[1]):
                        StrValue.append(s.split(':')[0])
                # filter the value accroding to string Name and the list of the value for this name
                qStringInside = InfluencingFactor.objects.filter(qName, Value__in=StrValue).values(
                    'ProductId_id').distinct()

                # combine the string list values and filter the data according to that
                if (cs > 0):
                    if (InfoStrOpEncoded[cs] == 'And'):
                        qString = qString.filter(ProductId_id__in=qStringInside)
                    else:
                        qString = qString | qStringInside
                else:
                    qString = qStringInside  # if the string list include only one item or first time intialization
                cs = cs + 1  # to access the correct index of the operation between strings list

            # create the result of the date list
            # encode the date lists
            InfoValDate1Encoded = [x.encode('UTF8') for x in listdate1]
            InfoValDate2Encoded = [x.encode('UTF8') for x in listdate2]
            InfoDateEncoded = [x.encode('UTF8') for x in listinfDa]
            InfoDateOpEncoded = [x.encode('UTF8') for x in operationDate]
            InfoDate1OpEncoded = [x.encode('UTF8') for x in OperationDate1]

            cda = 0;
            qDateInside = Q()
            for date in InfoDateEncoded:
                qn = Q(Name=date)
                qSD = InfoValDate1Encoded[cda]
                qED = InfoValDate2Encoded[cda]
                if (qSD and qED):
                    qDateInside = InfluencingFactor.objects.filter(qn, Value__range=(qSD, qED)).values(
                        'ProductId_id').distinct()
                elif qSD:
                    if (InfoDate1OpEncoded[cda] == 'lessThan'):
                        qv1 = Q(Value__lt=(InfoValDate1Encoded[cd]))
                        qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                    elif (InfoDate1OpEncoded[cda] == 'lessThanEqual'):
                        qv1 = Q(Value__lte=(InfoValDate1Encoded[cd]))
                        qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                    elif (InfoDate1OpEncoded[cda] == 'greater'):
                        qv1 = Q(Value__gt=(InfoValDate1Encoded[cd]))
                        qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                    elif (InfoDate1OpEncoded[cda] == 'greaterThanEqual'):
                        qv1 = Q(Value__gte=(InfoValDate1Encoded[cd]))
                        qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                    elif (InfoDate1OpEncoded[cda] == 'Equal'):
                        qv1 = Q(Value=(InfoValDate1Encoded[cda]))
                        qDateInside = InfluencingFactor.objects.filter(qn & qv1).values('ProductId_id').distinct()
                    else:
                        qDateInside = InfluencingFactor.objects.filter(qn, Value=qSD).values('ProductId_id').distinct()
                if (cda > 0):
                    if (InfoDateOpEncoded[cda] == 'And'):
                        qDate = qDate.filter(ProductId_id__in=qDateInside)
                    else:
                        qDate = qDate | qDateInside
                else:
                    qDate = qDateInside  # if the string list include only one item or first time intialization
                    cda = cda + 1  # to access the c

            OperationDeSEncode = [x.encode('UTF8') for x in operationDeS]
            operationSDEncode = [x.encode('UTF8') for x in operationSD]

            QGroup = Q()
            if (OperationDeSEncode[0] == 'Or' and qString):
                QGroup = qdecimal | qString
            else:
                if (qdecimal and qString):
                    QGroup = qdecimal.filter(ProductId_id__in=qString)
                elif qdecimal:
                    QGroup = qdecimal
                else:
                    QGroup = qString

            if (operationSDEncode[0] == 'Or' and qDate):
                QGroup = QGroup | qDate
            else:
                if (QGroup and qDate):
                    QBatch = QGroup.filter(ProductId_id__in=qDate)
                elif QGroup:
                    QGroup = QGroup
                else:
                    QGroup = qDate

            ##QGroupProduct = Product.objects.filter(id__in=QGroup)

            # save group details with influencing factor to batchinfluencingFactortable
            groupCriteria = GroupInfluencingFactorCriteria()
            groupCriteria.GroupId = group
            groupCriteria.DateList = InfoDateEncoded
            groupCriteria.DateValue1List = InfoValDate1Encoded
            groupCriteria.DateValue2List = InfoValDate2Encoded
            groupCriteria.DateOpList = InfoDateOpEncoded
            groupCriteria.Date1OpList = InfoDate1OpEncoded
            groupCriteria.StringDateOplist = operationSDEncode
            groupCriteria.StringList = InfoStrEncoded
            groupCriteria.StringOpList = InfoStrOpEncoded
            groupCriteria.StringValueList = InfoStrValEncoded
            groupCriteria.DecStringOpList = OperationDeSEncode
            groupCriteria.DecimalList = infoDecEncoded
            groupCriteria.DecimalOp1List = infoDecOpVal1wEncoded
            groupCriteria.DecimalOp2List = infoDecOpVal2wEncoded
            groupCriteria.DecimalVal1List = infoDecValue1Encoded
            groupCriteria.DecimalVal2List = infoDecValue2Encoded
            groupCriteria.DecimalBetOp = infoDecOpBetwEncoded
            groupCriteria.save()

            ProductInBatches = BatchProduct.objects.filter(BatchId_id__in=groupBatches,
                                                           ProductId__qualityfeature__Name=qFeature,
                                                           ProductId__in=QGroup) \
                .values('id', 'BatchId__BatchDescription', 'BatchId__BatchName', 'BatchId_id',
                        'ProductId__Name', 'ProductId__ExportDate', 'ProductId__LSL', 'ProductId__USL',
                        'ProductId__qualityfeature__Name', 'ProductId__qualityfeature__Value', 'ProductId_id')

            ProductInBatchesC = ProductInBatches.values('BatchId_id', 'ProductId__Name').order_by('BatchId_id',
                                                                                                  'ProductId__Name').annotate(
                total=Count('ProductId__Name'))

            # save the group with the product and batch that belong to it

        else:
            ProductInBatches = BatchProduct.objects.filter(BatchId_id__in=groupBatches,
                                                           ProductId__qualityfeature__Name=qFeature) \
                .values('id', 'BatchId__BatchDescription', 'BatchId__BatchName', 'BatchId_id',
                        'ProductId__Name', 'ProductId__ExportDate', 'ProductId__LSL', 'ProductId__USL',
                        'ProductId__qualityfeature__Name', 'ProductId__qualityfeature__Value', 'ProductId_id')

            ProductInBatchesC = ProductInBatches.values('BatchId_id', 'ProductId__Name').order_by('BatchId_id',
                                                                                                  'ProductId__Name').annotate(
                total=Count('ProductId__Name'))

        # Load Page data
        QFeature = QualityFeature.objects.values('Name').distinct()
        batches = Batch.objects.values('id', 'BatchName', 'BatchDescription').order_by('BatchName', 'BatchDescription',
                                                                                       'id')
        infLD = InfluencingFactor.objects.filter(Type="Decimal").values('Name').order_by('Name').distinct()
        infLS = InfluencingFactor.objects.filter(Type="String").values('Name').order_by('Name').distinct()
        infSV = InfluencingFactor.objects.filter(Type="String").values('Name', 'Value').order_by('Name',
                                                                                                 'Value').distinct()
        infLDT = InfluencingFactor.objects.filter(Type="Date").values('Name').order_by('Name').distinct()
        return render(request, 'group.html',
                      {'infLD': infLD, 'infLS': infLS, 'infLDT': infLDT, 'infSV': infSV, 'batches': batches,
                       'ProductInBatches': ProductInBatches, 'QFeature': QFeature,
                       'ProductInBatchesC': ProductInBatchesC, 'groups': group})
    elif request.method == 'POST' and 'SubmitGroupProductDetail' in request.POST:
        groupId = request.POST.get('GroupId')
        QualityFeatureName = request.POST.get('QualityFName')
        productId = request.POST.getlist('ProductId')
        batchId = request.POST.getlist('BatchId')
        selectPro = request.POST.get('Noselect')
        SampleNo = request.POST.get('SampleN')

        BatchProductList = []
        if ((SampleNo == '1' or SampleNo == '') and selectPro == '1'):
            # BatchProductWithOrderNum=BatchProduct.objects.filter(id__in=productId).values('BatchId','ProductId__Name','ProductId').annotate(Min('ProductId__OrderNum')).order_by('BatchId','ProductId__Name')
            BatchProducts = BatchProduct.objects.filter(id__in=productId, ProductId__SampleNum=1).values(
                'BatchId', 'ProductId__Name', 'ProductId')
        elif ((SampleNo == '') and selectPro != '1'):
            BatchProducts = BatchProduct.objects.filter(id__in=productId, ProductId__SampleNum=1).values(
                'BatchId', 'ProductId__Name', 'ProductId')
        elif (SampleNo > 1 and selectPro == '1'):
            BatchProductWithSampleNum = BatchProduct.objects.filter(id__in=productId,
                                                                    ProductId__SampleNum=SampleNo).values(
                'ProductId__Name').order_by('ProductId__Name')

            BatchProducts = BatchProduct.objects.filter(id__in=productId, ProductId__Name__in=BatchProductWithSampleNum,
                                                        ProductId__SampleNum__lte=SampleNo).values(
                'BatchId', 'ProductId__Name', 'ProductId', 'ProductId__SampleNum')
        elif (SampleNo > 1 and selectPro != '1'):
            SP = request.POST.getlist('SelectedBatchProduct')
            BatchProducts = BatchProduct.objects.filter(id__in=SP).values(
                'BatchId', 'ProductId__Name', 'ProductId')

        BatchPList = []
        for p in BatchProducts:
            groupProduct = GroupProduct()
            groupProduct.GroupId_id = groupId
            groupProduct.ProductId_id = p['ProductId']
            groupProduct.BatchId_id = p['BatchId']
            # qf= QualityFeature.objects.get(ProductId_id=p['ProductId'],Name=QualityFeatureName)
            groupProduct.QualityFeatureId = QualityFeature.objects.get(ProductId_id=p['ProductId'],
                                                                       Name=QualityFeatureName)
            BatchPList.append(groupProduct)
        GroupProduct.objects.bulk_create(BatchPList)

        batches = Batch.objects.values('id', 'BatchName', 'BatchDescription').order_by('BatchName', 'BatchDescription',
                                                                                       'id')
        QFeature = QualityFeature.objects.values('Name').distinct()
        infLD = InfluencingFactor.objects.filter(Type="Decimal").values('Name').order_by('Name').distinct()
        infLS = InfluencingFactor.objects.filter(Type="String").values('Name').order_by('Name').distinct()
        infSV = InfluencingFactor.objects.filter(Type="String").values('Name', 'Value').order_by('Name',
                                                                                                 'Value').distinct()
        infLDT = InfluencingFactor.objects.filter(Type="Date").values('Name').order_by('Name').distinct()

        return render(request, 'group.html',
                      {'infLD': infLD, 'infLS': infLS, 'infLDT': infLDT, 'infSV': infSV, 'batches': batches,
                       'QFeature': QFeature})
    else:
        batches = Batch.objects.values('id', 'BatchName', 'BatchDescription').order_by('BatchName', 'BatchDescription',
                                                                                       'id')
        QFeature = QualityFeature.objects.values('Name').distinct()
        infLD = InfluencingFactor.objects.filter(Type="Decimal").values('Name').order_by('Name').distinct()
        infLS = InfluencingFactor.objects.filter(Type="String").values('Name').order_by('Name').distinct()
        infSV = InfluencingFactor.objects.filter(Type="String").values('Name', 'Value').order_by('Name',
                                                                                                 'Value').distinct()
        infLDT = InfluencingFactor.objects.filter(Type="Date").values('Name').order_by('Name').distinct()

        return render(request, 'group.html',
                      {'infLD': infLD, 'infLS': infLS, 'infLDT': infLDT, 'infSV': infSV, 'batches': batches,
                       'QFeature': QFeature})


def visualization(request):
    group = Group.objects.all()
    if request.method == 'POST':
        groupId = request.POST.get('Group')
        groupIDG = groupId
        # groupAverage = BatchAverage.aggregate(sum('QualityFeatureId__Value')) / BatchAverage.count()
        Session.objects.all().delete()
        s = SessionStore()
        s['group'] = groupId
        s.save()
        graph2 = Graph()
        context = graph2.get_context_data()
        return render(request, 'visualization.html', context)
    return render(request, 'visualization.html', {'group': group})





class Graph(TemplateView):
    template_name = 'plot.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        s = Session.objects.all().order_by()[0]
        groupID = s.session_data
        group = s.get_decoded()

        if (group):
            ProductDetails = GroupProduct.objects.filter(GroupId_id=group['group']).values('ProductId__Name',
                                                                                           'QualityFeatureId__Value',
                                                                                           'QualityFeatureId__Name',
                                                                                           'GroupId__GroupName',
                                                                                           'BatchId__BatchName',
                                                                                           'SampleNo',
                                                                                           'ProductId__ExportDate').order_by(
                'ProductId__ExportDate')
        else:
            groupID = GroupProduct.objects.values('GroupId_id').order_by('GroupId_id')[0]
            ProductDetails = GroupProduct.objects.filter(GroupId_id=groupID['GroupId_id']).values('ProductId__Name',
                                                                                                  'QualityFeatureId__Value',
                                                                                                  'QualityFeatureId__Name',
                                                                                                  'GroupId__GroupName',
                                                                                                  'BatchId__BatchName',
                                                                                                  'SampleNo',
                                                                                                  'ProductId__ExportDate').order_by(
                'ProductId__ExportDate')

        h = ProductDetails.count();
        DProduct = ProductDetails.values('ProductId__Name').order_by('ProductId__Name').distinct()
        DBatch = ProductDetails.values('BatchId__BatchName').order_by('BatchId__BatchName').distinct()
        DGroup = ProductDetails.values('GroupId__GroupName').distinct()[0]
        DQName = ProductDetails.values('QualityFeatureId__Name').distinct()[0]
        SampleNum = ProductDetails.values('SampleNo').distinct()[0]
        DBatchC = DBatch.count()
        DProductC = DProduct.count()

        w = 6;
        Matrix = [['' for x in range(w)] for y in range(h)]
        x = 0;
        value = []
        dateV = []
        BatchName = []
        ProductName=[]
        for p in ProductDetails:
            Matrix[x][0] = p['ProductId__Name']
            ProductName.append( Matrix[x][0])
            Matrix[x][1] = p['QualityFeatureId__Value']
            value.append(Matrix[x][1])
            Matrix[x][2] = p['BatchId__BatchName']
            BatchName.append(Matrix[x][2])
            Matrix[x][3] = p['ProductId__ExportDate']
            dateV.append(Matrix[x][3])
            x = x + 1

        BatchAverage = []
        ProductAverage = []
        count = 0;
        for b in DBatch:
            Pcount = 0;
            if (SampleNum['SampleNo'] == 1):
                ProductBatchTotalVal = ProductDetails.filter(BatchId__BatchName=b['BatchId__BatchName']).aggregate(
                    Avg('QualityFeatureId__Value'))
                BatchAverage.append(ProductBatchTotalVal)
                count = count + 1
            elif (SampleNum['SampleNo'] != 1):
                for pi in DProduct:
                    ProductTotal = ProductDetails.filter(BatchId__BatchName=b['BatchId__BatchName'],
                                                         ProductId__Name=pi['ProductId__Name']).aggregate(
                        Avg('QualityFeatureId__Value'))
                    if(ProductTotal['QualityFeatureId__Value__avg']) :
                         ProductAverage.append(ProductTotal['QualityFeatureId__Value__avg'])
                         Pcount = Pcount + 1
                BatchAverage.append((sum(ProductAverage)/Pcount))
                count = count + 1

        if (SampleNum['SampleNo'] == 1):
            groupAverage = sum(item['QualityFeatureId__Value__avg'] for item in BatchAverage) / count
        else:
            groupAverage = sum(BatchAverage) / count

            # ProductDetails = request.session.get('group')
        x = dateV
        y = value


        size = len(x)
        yaverage = []
        for i in x:
            yaverage.append(groupAverage)
        trace0 = go.Scatter(x=x, y=y, marker={'color': '#179c81'}, text=BatchName,
                            mode="lines+markers", name='1st Trace')
        trace1 = go.Scatter(x=x, y=yaverage, marker={'color': 'Red'}, mode="lines", name='Mean')
        data = [trace0, trace1]
        layout = go.Layout(title=DGroup['GroupId__GroupName'], xaxis={'title': 'Export Date'},
                           yaxis={'title': DQName['QualityFeatureId__Name']})
        figure = go.Figure(data=data, layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        # Create Overal Distribution graph


        data = [go.Histogram(x=y, histnorm='probability')]


        divOv = opy.plot(data, filename='normalized histogram', auto_open=False, output_type='div')


        context['graph'] = div

        context['group'] = Group.objects.all()

        context['graphOv'] = divOv


        import plotly.plotly as py  # tools to communicate with Plotly's server

        fig = plt.figure()

        # example data
        mu = float(np.mean(y))  # mean of distribution
        sigma = float(np.std(y, ddof=1))   # standard deviation of distribution
        a = np.array(y, dtype=float)


        # the histogram of the data
        n, bins, patches = plt.hist(a,len(a), normed=1, facecolor='blue',alpha=0.75)
        # add a 'best fit' line
        y = mlab.normpdf(bins, mu,sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Value')
        plt.ylabel('Probability')

        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)

        plot_url = opy.plot_mpl(fig, filename='Normal Distribution', auto_open=False, output_type='div')

        context['graphCurve'] = plot_url

        return context
