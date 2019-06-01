import datetime
import time
from django import template

register = template.Library()


@register.filter
def format_date(value):
    # Ваш код
    time_now = time.time()
    delta = float(time_now) - float(value)
    if delta < 600:
        return "Только что"
    elif delta >= 600 and delta < 86400:
        return f'{round(delta/3600)} часов назад'
    else:
        return datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d')


@register.filter
def format_score(value="Unknown"):
    if int(value) <= -5:
        return "Very very bad :("
    elif int(value)in range(-5, 5):
        return "Not bad"
    elif int(value) >= 5:
        return "Excelent"
    else:
        return value


@register.filter
def format_num_comments(value):
    # Ваш код
    if int(value) == 0:
        return "Leave the comment"
    elif int(value) in range(0, 50):
        return value
    else:
        return "50+"

# Оставляет count первых и count последних слов, между ними должно быть троеточие.
# count задается параметром фильтра. Пример c count = 5: "Hi all sorry if this ... help or advice greatly appreciated."
#
# Знаки препинания остаются, обрезаются только слова.
@register.filter
def format_selfcomments(value, count):
    if value:
        list_value = value.split(' ')
        return f'{" ".join(list_value[:count])}...{" ".join(list_value[:-count-1:-1])}'
    return "No info..."
