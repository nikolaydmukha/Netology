import datetime
import os
from .settings import BASE_DIR
from django.shortcuts import render
from django.shortcuts import render_to_response


def file_list(request):
    print(request.GET)
    template_name = 'index.html'
    files_list = os.listdir(os.path.join(BASE_DIR, 'files'))
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    print("FILE_LIST---1")
    context = dict()
    # Читаем все файлы из директории files
    files = list()
    tmp_dict = dict()
    for f in files_list:
        meta = os.stat(os.path.join(BASE_DIR, f'files/{f}'))
        # Дата создания
        year_cr, month_cr, day_cr = datetime.datetime.utcfromtimestamp(meta.st_ctime).strftime("%Y, %m, %d").split(',')
        # Дата измененеия
        year_ch, month_ch, day_ch = datetime.datetime.utcfromtimestamp(meta.st_mtime).strftime("%Y, %m, %d").split(',')
        tmp_dict = {
            'name': f,
            'ctime': datetime.datetime(int(year_cr), int(month_cr), int(day_cr)),
            'mtime': datetime.datetime(int(year_ch), int(month_ch), int(day_ch))
        }
        files.append(tmp_dict)
    context = {'files': files, 'date': datetime.date(2019, 5, 19)}
    # Сформируем context в зависимости от фильтр-даты "date"

    print("CONTEXT----------", context)
    return render(request, template_name, context)


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    with open(os.path.join(BASE_DIR, f'files/{name}')) as file:
        data = file.read()
    files = {
        name: {
            'file_content': data
        }
    }
    context = {'name': name, 'file_content': files[name]['file_content']}
    return render(request, 'file_content.html', context)
