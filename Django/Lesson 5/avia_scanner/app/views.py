import time
import random

from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

from .models import City
from .forms import SearchTicket
from .models import City


def ticket_page_view(request):
    template = 'app/ticket_page.html'

    context = {
        'form': SearchTicket()
    }

    return render(request, template, context)


def cities_lookup(request):
    look_for = request.GET.get('term')
    key_cache = look_for.lower()
    results = cache.get(key_cache)

    if results is None:
        results = []
        cities = City.objects.all()
        for city in cities:
            if look_for in city.name.lower():
                results.append(city.name)
        cache.set(key_cache, results)

    return JsonResponse(results, safe=False)
