from django.shortcuts import render
from . models import Phone, Samsung, Iphone
from django.db import connection


def show_catalog(request):
    template = 'catalog.html'
    iphones = Iphone.objects.all().values('name__name', 'applepay', 'faceid', 'name__cam', 'name__os', 'name__price',
                                         'name__display', 'name__weight')
    samsungs = Samsung.objects.all().values('name__name', 'samsungpay', 'fm', 'ikport', 'name__cam', 'name__os',
                                            'name__price', 'name__display', 'name__weight')
    context = {
        'iphones': iphones,
        'samsungs': samsungs,
        }
    return render(request, template, context)
