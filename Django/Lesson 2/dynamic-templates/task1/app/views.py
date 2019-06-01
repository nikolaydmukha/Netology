import csv
import os

from django.shortcuts import render
from .settings import BASE_DIR

def inflation_view(request):
    template_name = 'inflation.html'
    data = dict()
    inflation_data = list()
    with open(os.path.join(BASE_DIR, 'inflation_russia.csv'), encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for csv_data in reader:
            data[csv_data['Год']] = dict()
            row_names = ['Янв', 'Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек', 'Суммарная']
            for row in row_names:
                if csv_data[row] != '':
                    data[csv_data['Год']][row] = float(csv_data[row])
                else:
                    data[csv_data['Год']][row] = csv_data[row]
    context = {'data': data}
    return render(request, template_name, context)
