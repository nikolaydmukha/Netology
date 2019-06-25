from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    # ID продукта
    product_id = request.path.lstrip("/product/").rstrip("/")
    if 'reviewed_products' not in request.session:
        request.session['reviewed_products'] = []
    # Получим все отзывы
    reviews = Review.objects.all().filter(product=Product.objects.get(id=product_id))
    form = ReviewForm
    if request.method == 'POST':
        # Запишем в сессию, что сделали отзыв продукту
        request.session['reviewed_products'].append(product_id)
        request.session.save()
        review_text = request.POST['text']  # отзыв
        review = Review(text=review_text, product=Product.objects.get(id=product_id))  # запись отзыва в БД
        review.save()

    if product_id not in request.session['reviewed_products']:
        context = {
            'form': form,
            'product': product,
            'reviews': reviews
        }
        return render(request, template, context)
    context = {
        'product': product,
        'is_review_exist': True,
        'reviews': reviews
    }
    return render(request, template, context)
