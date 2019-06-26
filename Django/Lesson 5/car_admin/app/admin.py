from django.contrib import admin

from .models import Car, Review
from .forms import ReviewAdminForm


class CarAdmin(admin.ModelAdmin):
    # список полей, отображаемых в админке
    list_display = ['brand', 'model', 'get_reviews']
    # список полей, по которым осуществляется поиск
    search_fields = ['brand', 'model']
    # филтьтр
    list_filter = ('brand',)
    # порядок сортировки
    ordering = ('-id',)


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    # список полей, отображаемых в админке
    list_display = ['car', 'title']
    # список полей, по которым осуществляется поиск
    search_fields = ['car__brand', 'car__model']
    # порядок сортировки
    ordering = ('-id',)


admin.site.register(Car, CarAdmin)
admin.site.register(Review, ReviewAdmin)
