from django.db import models


class Tags(models.Model):
    name = models.CharField(max_length=64, null=True, verbose_name='Название тега')

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    tags = models.ManyToManyField(Tags, through='ArticleTags')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class ArticleTags(models.Model):
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    isMain = models.BooleanField(default=False, verbose_name='Основной')

