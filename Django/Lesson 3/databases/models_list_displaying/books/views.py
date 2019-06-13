from django.shortcuts import render
from . models import Book
from django.db import connection


def books_view(request):
    context = {}
    template = 'books/books_list.html'
    if request.path == "/books/" or request.path == "/":
        all_data = Book.objects.all()
        context = {
            "books": all_data,
        }
        return render(request, template, context)
    datefromurl = request.path.rstrip('/')[-10:]
    booksmonthdate = Book.objects.filter(pub_date__icontains=datefromurl[:7:])
    page_count = booksmonthdate.count()  # число страниц с книгами для пагинации
    counter = 1
    context_list = list()
    if page_count == 1:
        context = {
            'prev_page_url': None,
            'next_page_url': None,
            'current_page': 1,
            'books': booksmonthdate[0],
        }
        context_list.append(context)
        return render(request, template, context)
    else:
        while counter <= page_count:
            if counter == 1:
                condition_one = counter + 1
                context = {
                    'prev_page_url': None,
                    'next_page_url': f'?page={condition_one}',
                    'current_page': 1,
                    'books': booksmonthdate[counter-1],
                }
                context_list.append(context)
            elif counter == page_count:
                condition_two_prev = counter - 1
                context = {
                    'prev_page_url': f'?page={condition_two_prev}',
                    'next_page_url': None,
                    'current_page': counter,
                    'books': booksmonthdate[counter-1],
                }
            else:
                condition_three_prev = counter - 1
                condition_three_next = counter + 1
                context = {
                    'prev_page_url': f'?page={condition_three_prev}',
                    'next_page_url': f'?page={condition_three_next}',
                    'current_page': counter,
                    'books': booksmonthdate[counter-1],
                }
            context_list.append(context)
            counter += 1
    if page_count > 1:
        print("СТРАНИЦ МНОГОООО!!!! !!!!!!", request.GET)
        if 'page' in request.GET:
            print("YES    PAGE!!!!!!", request.GET)
            return render(request, template, context=context_list[int(request.GET['page'])])
        k = [i for i in range(len(context_list)) if str(context_list[i]['books'].pub_date) == datefromurl]
        return render(request, template, context=context_list[k[0]])
    return render(request, template, context=context_list[0])
