import datetime
from django.db import models


# Тэги
class Tags(models.Model):
    name = models.CharField(max_length=32, null=True, verbose_name='Название тега')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


# Авторы
class AuthorsList(models.Model):
    name = models.CharField(max_length=64, null=True, verbose_name='Автор')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


# Жанры
class Genre(models.Model):
    name = models.CharField(verbose_name='Жанр', max_length=32, null=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


# Шкафы
class Cupboard(models.Model):
    cupboard = models.IntegerField(verbose_name='Номер шкафа')

    class Meta:
        verbose_name = 'Шкаф'
        verbose_name_plural = 'Шкафы'

    def __str__(self):
        return str(self.cupboard)


# Полки
class Shelf(models.Model):
    shelf = models.IntegerField(verbose_name='Номер полки')

    class Meta:
        verbose_name = 'Полка'
        verbose_name_plural = 'Полки'

    def __str__(self):
        return str(self.shelf)


# Номера мест на полке
class ShelfPlace(models.Model):
    shelfplace = models.IntegerField(verbose_name='Номер полки')

    class Meta:
        verbose_name = 'Номер на полке'
        verbose_name = 'Номера на полках'

    def __str__(self):
        return str(self.shelfplace)


# Читатели
class Reader(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=64)
    phone = models.CharField(verbose_name='Номер телефона', max_length=12, blank=True)
    address = models.TextField(verbose_name='Адрес', blank=True)
    notes = models.TextField(verbose_name='Заметки', blank=True)

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'

    def __str__(self):
        return self.name


# Книги
class Books(models.Model):
    title = models.CharField(verbose_name='Название книги', max_length=64)
    author = models.ForeignKey(AuthorsList, default="", blank=True, on_delete=models.CASCADE, verbose_name='Автор')
    published_date = models.DateTimeField(verbose_name='Дата публикации')
    genre = models.ForeignKey(Genre,  on_delete=models.CASCADE, verbose_name='Жанр')
    cupboard = models.ForeignKey(Cupboard, on_delete=models.CASCADE, verbose_name='Шкаф', related_name='book_cupboard')
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, verbose_name='Полка', related_name='book_shelf')
    place = models.ForeignKey(ShelfPlace, on_delete=models.CASCADE, verbose_name='Место на полке', related_name='book_place')
    tags = models.ManyToManyField(Tags, verbose_name='Название тега')
    reader = models.ForeignKey(Reader,  blank=True, null=True, default="", on_delete=models.CASCADE, verbose_name='Читатель')
    get_date = models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Книга выдана')
    expire_date = models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name='Сдать до')
    isfree = models.BooleanField(verbose_name='В наличии', default=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title



