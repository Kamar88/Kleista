from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import xlrd, os
from models import Product, InfluencingFactor, QualityFeature, Group, Batch, BatchInfluencingFactor, GroupBatches
import datetime
from decimal import *


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
                    ifc.Value =datetime.datetime(*xlrd.xldate_as_tuple(xl_sheet.cell_value(row, int(Date[0])), book.datemode))
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
    return render(request, "Batch.html", {})


def group(request):
    return render(request, "group.html", {})


def visualization(request):
    return render(request, "visualization.html", {})
