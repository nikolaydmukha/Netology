
from datetime import datetime, timedelta

from django import forms

from .widgets import AjaxInputWidget
from .models import City


class SearchTicket(forms.Form):
    departure = forms.CharField(widget=AjaxInputWidget(url='api/city_ajax'), label='Город отправления')
    arrived = forms.ModelChoiceField(queryset=City.objects.all(), label='Город назначения')
    depart_at = forms.DateField(widget=forms.SelectDateWidget, initial=datetime.today() + timedelta(days=14))
