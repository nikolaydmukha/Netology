from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()

def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    if 'stat' not in request.GET:
        if ('from-landing' not in request.GET):
            counter_click['all'] += 1
        else:
            if request.GET['from-landing'] == 'original':
                counter_show['original'] += 1
                counter_click['all'] += 1
            else:
                counter_show['test'] += 1
                counter_click['all'] += 1
        context = {
            'all': counter_click['all'],
            'original': counter_show['original'],
            'test': counter_show['test']
        }
        print("CONTEXT", context)
        return render_to_response('index.html', context)
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    if 'ab-test-arg' not in request.GET:
        return render_to_response('stats.html')
    elif request.GET['ab-test-arg'] == 'landing':
        return render_to_response('landing.html')
    elif request.GET['ab-test-arg'] == 'test':
        return render_to_response('landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    context = {
        'test_conversion': round(int(request.GET['test'])/int(request.GET['all']),1),
        'original_conversion': round(int(request.GET['original'])/int(request.GET['all']),1),
    }

    return render_to_response('stats.html', context)
