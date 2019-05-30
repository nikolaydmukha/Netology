import csv
from pprint import pprint

from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from .settings import BUS_STATION_CSV

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(BUS_STATION_CSV, encoding='cp1251') as file:
        reader = csv.DictReader(file)
        tmp_dict = dict()
        tmp_list = list()
        for raw in reader:
            tmp_dict = {
                'Name': raw['Name'],
                'Street': raw['Street'],
                'District': raw['District']
            }
            tmp_list.append(tmp_dict)
        context = {
            'prev_page_url': None,
            'next_page_url': None,
        }
        page_count = len(tmp_list)
    counter = 1
    context_list = list()
    while counter <= round(page_count/10):
        if counter == 1:
            condition_one = counter + 1
            context = {
                'prev_page_url': None,
                'next_page_url': f'?page={condition_one}',
                'current_page': 1,
                'bus_stations': tmp_list[0:10:1],
            }
            context_list.append(context)
        elif counter == round(page_count/10):
            condition_two_prev = counter - 1
            context = {
                'prev_page_url': f'?page={condition_two_prev}',
                'next_page_url': None,
                'current_page': counter,
                'bus_stations': tmp_list[counter*10:counter*10+10:1],
            }
        else:
            condition_three_prev = counter - 1
            condition_three_next = counter + 1
            context = {
                'prev_page_url': f'?page={condition_three_prev}',
                'next_page_url': f'?page={condition_three_next}',
                'current_page': counter,
                'bus_stations': tmp_list[counter*10:counter*10+10:1],
            }
        context_list.append(context)
        counter += 1
    if 'page' in request.GET:
        return render_to_response('index.html', context=context_list[int(request.GET['page'])])
    return render_to_response('index.html', context=context_list[1])
