from django.views.generic import ListView
from django.shortcuts import render

from .models import Article, Author


def articles_list(request):
    template_name = 'articles/news.html'
    context = {}
    articles = Article.objects.all().select_related("author").only('author__name', 'genre', 'title', 'text')
    context = {'articles': articles}

    return render(request, template_name, context)
