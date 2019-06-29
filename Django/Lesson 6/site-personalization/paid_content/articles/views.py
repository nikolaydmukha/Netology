from django.shortcuts import render
from .models import Article, Profile


def show_articles(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,

    }
    return render(
        request,
        'articles.html',
        context
    )


def show_article(request, id):
    # Проверим, открыт ли пользователю платный контент, если такой естт
    user_paid = False
    user = Profile.objects.filter(user=request.user)
    for value in user:
        user_paid = value.buy_paidcontent
    article = Article.objects.filter(id=id)
    context = {}
    for art in article:
        if art.is_paid and not user_paid:
            context = {
                'paid': 'Это платный контент. Необходима подписаться!'
            }
        context['article'] = article
    # Если нажата кнопка "Подписаться"
    print(request.method)
    if request.method == 'POST':
        Profile.objects.filter(user=request.user).update(buy_paidcontent=True)
    return render(
        request,
        'article.html',
        context
    )
