from django.contrib import admin
from .models import Books, AuthorsList, Shelf, Tags, Reader, Genre, Cupboard, ShelfPlace


class BooksAdmin(admin.ModelAdmin):
    # список полей, отображаемых в админке
    list_display = ['title', 'author', 'cupboard', 'shelf', 'place', 'reader', 'expire_date', 'isfree']
    # список полей, по которым осуществляется поиск
    search_fields = ['title', 'author__name', 'reader__name']

    # порядок сортировки
    ordering = ('title', 'author')
    # действие по возврату всех книг пользователя
    actions = ['return_books', ]

    def return_books(self, request, queryset):
        queryset.update(isfree=True, reader="")
    return_books.short_description = "Вернуть выбранные книги"


class ReaderAdmin(admin.ModelAdmin):
    # список полей, отображаемых в админке
    list_display = ['name', 'phone', 'address']
    # список полей, по которым осуществляется поиск
    search_fields = ['name', ]

    # порядок сортировки
    ordering = ('name',)


admin.site.register(Books, BooksAdmin)
admin.site.register(AuthorsList)
admin.site.register(Shelf)
admin.site.register(Tags)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Cupboard)
admin.site.register(ShelfPlace)
admin.site.register(Genre)

