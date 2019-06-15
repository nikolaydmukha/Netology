from django.shortcuts import render
from django.db import connection
from .models import Phone

def show_catalog(request):
    template = 'catalog.html'
    all_phones = Phone.objects.all()
    if 'sort' in request.GET:
        if request.GET['sort'] == 'name':
            all_phones = Phone.objects.all().order_by('name')
        elif request.GET['sort'] == 'max_price':
            all_phones = Phone.objects.all().order_by('-price')
        else:
            all_phones = Phone.objects.all().order_by('price')
    context = {'all_phones': all_phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_info = Phone.objects.all().filter(slug=slug)
    context = {'phone_info': phone_info}
    return render(request, template, context)
