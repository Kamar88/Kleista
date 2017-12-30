from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import xlrd, os
from models import Product, InfluencingFactor, QualityFeature, Group, Batch, BatchInfluencingFactor, GroupBatches
import datetime
from decimal import *
from django.db.models import Q


def home(request):
    if request.method == 'POST' and 'reset' in request.POST:
        Product.objects.all().delete()
        InfluencingFactor.objects.all().delete()
        QualityFeature.objects.all().delete()
        Group.objects.all().delete()
        Batch.objects.all().delete()
        BatchInfluencingFactor.objects.all().delete()
        GroupBatches.objects.all().delete()
    elif (request.method == 'POST' and 'DataTable' in request.POST) or (
                    request.method == 'POST' and 'SubmitList' in request.POST):
        productc = Product.objects.all().count()
        if productc > 0:
            Product.objects.all().delete()
            InfluencingFactor.objects.all().delete()
            QualityFeature.objects.all().delete()
            Group.objects.all().delete()
            Batch.objects.all().delete()
            BatchInfluencingFactor.objects.all().delete()
            GroupBatches.objects.all().delete()
        if request.method == 'POST' and 'DataTable' in request.POST:
            myfile = request.FILES['DataTableF']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            book = xlrd.open_workbook(settings.MEDIA_ROOT + "\\" + filename)
            xl_sheet = book.sheet_by_index(0)
            if xl_sheet.nrows > 0:
                row = xl_sheet.row(0)
                col_list = []
                for cnt in range(len(row)): col_list.append(row[cnt].value.encode('utf-8').strip())
                return render(request, 'Setup.html', {'ColList': col_list, 'File_Name': filename})
            else:
                uploaded_file_url = "The Data Table that you have uploaded is empty. Please Upload another Data Table"
                return render(request, 'Setup.html', {'uploaded_file_url': uploaded_file_url})
        elif request.method == 'POST' and 'SubmitList' in request.POST:
            productn = request.POST.getlist('ProductName')
            LSL = request.POST.getlist('LSL')
            USL = request.POST.getlist('USL')
            INF = request.POST.getlist('InflFactor')
            QF = request.POST.getlist('QFeature')
            filename = request.POST.get('FileName')
            Date = request.POST.getlist('Date')

            book = xlrd.open_workbook(settings.MEDIA_ROOT + "\\" + filename.encode('utf-8').strip())
            xl_sheet = book.sheet_by_index(0)

            for row in range(1, xl_sheet.nrows):
                product = Product()

                nrow = xl_sheet.nrows
                # Product details
                product.Name = xl_sheet.cell_value(row, int(productn[0])).encode('utf-8').strip()
                cell = xl_sheet.cell_value(row, int(productn[0])).encode('utf-8').strip()
                product.OrderNum = row
                product.SampleNum = 0
                type = xl_sheet.cell_type(row, int(productn[0]))
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
                    product.ExportDate = datetime.datetime(
                        *xlrd.xldate_as_tuple(xl_sheet.cell_value(row, int(Date[0])), book.datemode))
                else:
                    product.ExportDate = " "

                product.save()

                # QualityFeatures
                for QFI in QF:
                    qfc = QualityFeature()
                    qfc.Name = xl_sheet.cell_value(0, int(QFI)).encode('utf-8').strip()
                    type = xl_sheet.cell_type(row, int(QFI))
                    if (type == 2):
                        qfc.Value = Decimal(str(xl_sheet.cell_value(row, int(QFI))).encode('utf-8'))
                    else:
                        qfc.Value = 0
                    qfc.ProductId = product
                    qfc.save()

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
                    ifc.save()
                if len(Date):
                    ifc = InfluencingFactor()
                    ifc.Name = xl_sheet.cell_value(0, int(Date[0])).encode('utf-8').strip()
                    ifc.Type = "Date"
                    ifc.ProductId = product
                    ifc.Value = datetime.datetime(
                        *xlrd.xldate_as_tuple(xl_sheet.cell_value(row, int(Date[0])), book.datemode))
                    ifc.save()

            difPro = Product.objects.values('Name').distinct()

            for p in difPro:
                product = Product.objects.filter(Name=p['Name'])
                count = 1
                for ip in product:
                    ip.SampleNum = count
                    count = count + 1
                    ip.save()

    return render(request, 'Setup.html', {})
    return render(request, 'Setup.html', {})


def batch(request):
    if request.method == 'POST' and 'Submit' in request.POST:
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

        # StringList retriving
        listinfS = request.POST.getlist('InfS')  # retrive all the string lists from the batch page
        listinfSV = request.POST.getlist(
            'InfluencingFactorSV')  # retrive all the string value lists from the batch page
        operationS = request.POST.getlist('OperationS')  # retrive the operation between the String values

        operationDeS = request.POST.getlist('OperationDecString') #get the operation between decimal Lists and String Lists
        operationSD = request.POST.getlist('OperationStringDate') #get the operation between String Lists and date list 

        # save Batch details to database
        batch = Batch()
        batch.BatchName = BatchN
        batch.BatchDescription = BatchD

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
        InfoStrEncoded = [x.encode('UTF8') for x in listinfS] #It includes the string influencing factor names
        InfoStrValEncoded = [x.encode('UTF8') for x in listinfSV] #It includes the string influencing factor names with its value
        InfoStrOpEncoded = [x.encode('UTF8') for x in operationS] #It includes the operation between the string value

        qString = Q()
        cs = 0 ;

        #two loops to link the name of the string with its values and filter the influencing factor table.
        for name in InfoStrEncoded:
            qName = Q(Name=name) #build the filter criteria of the query by sitting the name first of all
            StrValue = []
            for s in InfoStrValEncoded: #checks all the value of the string name and append it is vale to list
                if (name == s.split(':')[1]):
                    StrValue.append(s.split(':')[0])
            #filter the value accroding to string Name and the list of the value for this name
            qStringInside = InfluencingFactor.objects.filter(qName, Value__in=StrValue).values('ProductId_id').distinct()

            #combine the string list values and filter the data according to that
            if(cs > 0):
                if(InfoStrOpEncoded[cs]=='And'):
                     qString = qString.filter(ProductId_id__in=qStringInside)
                else:
                    qString = qString | qStringInside
            else:
                qString = qStringInside #if the string list include only one item or first time intialization
            cs= cs +1 #to access the correct index of the operation between strings list

        #create the result of the date list
        #encode the date lists
        InfoValDate1Encoded = [x.encode('UTF8') for x in listdate1]
        InfoValDate2Encoded = [x.encode('UTF8') for x in listdate2]
        InfoDateEncoded = [x.encode('UTF8') for x in listinfDa]

        InfoDateOpEncoded = [x.encode('UTF8') for x in operationDate]

        cda= 0;
        for date in InfoDateEncoded :
            qn = Q(Name=date)
            qSD = InfoValDate1Encoded[cda]
            qED = InfoValDate2Encoded[cda]
            if(qSD and qED) :
                qDateInside = InfluencingFactor.objects.filter(qn, Value__range=(qSD, qED)).values('ProductId_id').distinct()
            else :
                qDateInside =  InfluencingFactor.objects.filter(qn,Value=qSD).values('ProductId_id').distinct()
            if (cda > 0):
                if (InfoStrOpEncoded[cda] == 'And'):
                    qDate = qDate.filter(ProductId_id__in=qDateInside)
                else:
                    qDate = qDate | qDateInside
            else:
                qDate = qDateInside  # if the string list include only one item or first time intialization
                cda = cda + 1  # to access the c



    # save batch details with influencing factor to batchinfluencingFactortable


    infLD = InfluencingFactor.objects.filter(Type="Decimal").values('Name').order_by('Name').distinct()
    infLS = InfluencingFactor.objects.filter(Type="String").values('Name').order_by('Name').distinct()
    infSV = InfluencingFactor.objects.filter(Type="String").values('Name', 'Value').order_by('Name', 'Value').distinct()
    infLDT = InfluencingFactor.objects.filter(Type="Date").values('Name').order_by('Name').distinct()

    return render(request, 'Batch.html', {'infLD': infLD, 'infLS': infLS, 'infLDT': infLDT, 'infSV': infSV})


def group(request):
    return render(request, "group.html", {})


def visualization(request):
    return render(request, "visualization.html", {})
