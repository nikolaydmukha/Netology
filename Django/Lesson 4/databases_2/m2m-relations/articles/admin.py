
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tags, ArticleTags


class ArticleTagsInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_ismain = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            form.cleaned_data
            if 'isMain' in form.cleaned_data and form.cleaned_data['isMain'] == True:
                count_ismain += 1
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if count_ismain != 1:
            raise ValidationError('Основным может бтыть один и только один тэг! Пожалуйста, поправьте ошибку')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleTagsInline(admin.TabularInline):
    model = ArticleTags
    formset = ArticleTagsInlineFormset



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleTagsInline]
    exclude = ('tags',)

admin.site.register(Tags)
