from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import xlrd, os
from models import Product, InfluencingFactor, QualityFeature


def home(request):
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
           return render(request, 'Setup.html', {'ColList':col_list,'File_Name': filename})
        else:
            uploaded_file_url = "The Data Table that you have uploaded is empty. Please Upload another Data Table"
            return render(request, 'Setup.html', {'uploaded_file_url': uploaded_file_url})
    elif request.method == 'POST' and 'SubmitList' in request.POST:
        productn= request.POST.getlist('ProductName')
        LSL = request.POST.getlist('LSL')
        USL = request.POST.getlist('USL')
        INF = request.POST.getlist('InflFactor')
        QF  = request.POST.getlist('QFeature')
        filename = request.POST.get('FileName')
        Date = request.POST.getlist('Date')

        value = int(productn[0])

        book = xlrd.open_workbook(settings.MEDIA_ROOT + "\\" + filename.encode('utf-8').strip())
        xl_sheet = book.sheet_by_index(0)

        product = Product()
        ifc = InfluencingFactor()
        qf = QualityFeature()


        for row in range(0, xl_sheet.nrows):
          product.Name = xl_sheet.cell_value(row + 1, int(productn[0]))

        return render(request, 'Setup.html',{})


    return render(request,'Setup.html', {})


def batch(request):
    return render(request, "Batch.html", {})


def group(request):
    return render(request, "group.html", {})


def visualization(request):
    return render(request, "visualization.html", {})
