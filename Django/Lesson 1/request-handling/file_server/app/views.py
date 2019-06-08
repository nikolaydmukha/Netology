import datetime
import os
from pprint import pprint

from django.http import HttpResponseNotFound

from .settings import BASE_DIR
from django.shortcuts import render
from django.shortcuts import render_to_response


def file_list(request):
    url = request.get_full_path()
    template_name = 'index.html'
    files_list = os.listdir(os.path.join(BASE_DIR, 'files'))
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    context = dict()
    # Читаем все файлы из директории files
    files = list()
    tmp_dict = dict()
    for f in files_list:
        meta = os.stat(os.path.join(BASE_DIR, f'files/{f}'))
        # Дата создания
        year_cr, month_cr, day_cr, hour_cr, min_cr = datetime.datetime.utcfromtimestamp(meta.st_ctime).strftime("%Y, %m, %d, %H, %m").split(',')
        # Дата измененеия
        year_ch, month_ch, day_ch, hour_ch, min_ch = datetime.datetime.utcfromtimestamp(meta.st_mtime).strftime("%Y, %m, %d, %H, %m").split(',')
        tmp_dict = {
            'name': f,
            'ctime': datetime.datetime(int(year_cr), int(month_cr), int(day_cr), int(hour_cr), int(min_cr)),
            'mtime': datetime.datetime(int(year_ch), int(month_ch), int(day_ch), int(hour_ch), int(min_ch))
        }
        print(datetime.datetime(int(year_cr), int(month_cr), int(day_cr), int(hour_cr), int(min_cr)))
        files.append(tmp_dict)
    if url == "/":
        context = {'files': files, 'date': None}
    else:
        year_parsed, month_parsed, day_parsed = url.strip("/").split("-")
        parsed_date = url.strip("/")
        for elem in files:
            if parsed_date != elem['ctime'].strftime("%Y-%m-%d"):
               files.remove(elem)
        context = {'files': files, 'date': datetime.date(int(year_parsed), int(month_parsed), int(day_parsed))}
    return render(request, template_name, context)


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    if os.path.isfile(f'files/{name}'):
        with open(os.path.join(BASE_DIR, f'files/{name}')) as file:
            data = file.read()
        files = {
            name: {
                'file_content': data
            }
        }
        context = {'name': name, 'file_content': files[name]['file_content']}
        return render(request, 'file_content.html', context)
    return HttpResponseNotFound("Файл не найден!")
