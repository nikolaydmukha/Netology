import datetime
import os
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
    if url == "/" or url == "/0000-00-00/":
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
        context = {'files': files, 'date': None}
    else:
        year_parsed, month_parsed, day_parsed = url.strip("/").split("-")
        for f in files_list:
            meta = os.stat(os.path.join(BASE_DIR, f'files/{f}'))
            # Дата создания
            year_cr, month_cr, day_cr = datetime.datetime.utcfromtimestamp(meta.st_ctime).strftime("%Y, %m, %d").split(
                ',')
            # Дата измененеия
            year_ch, month_ch, day_ch = datetime.datetime.utcfromtimestamp(meta.st_mtime).strftime("%Y, %m, %d").split(
                ',')
            if year_parsed == year_cr.strip() and month_parsed == month_cr.strip() and day_parsed == day_cr.strip():
                tmp_dict = {
                    'name': f,
                    'ctime': datetime.datetime(int(year_cr), int(month_cr), int(day_cr)),
                    'mtime': datetime.datetime(int(year_ch), int(month_ch), int(day_ch))
                }
                files.append(tmp_dict)
        context = {'files': files, 'date': datetime.date(int(year_parsed), int(month_parsed), int(day_parsed))}
    # Сформируем context в зависимости от фильтр-даты "date"
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
