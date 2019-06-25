from django import forms


class CalcForm(forms.Form):
    initial_fee = forms.IntegerField(label="Стоимость товара")
    rate = forms.FloatField(label="Процентная ставка")
    months_count = forms.IntegerField(label="Срок кредита в месяцах", min_value=1, max_value=12)

    def clean_initial_fee(self):
        initial_fee = self.cleaned_data.get('initial_fee')
        if not initial_fee or initial_fee <= 0:
            raise forms.ValidationError("Стоимость товара не может быть отрицательной или равной нули!")
        return initial_fee

    def clean_rate(self):
        rate = self.cleaned_data.get('rate')
        if not rate or (rate not in range(0, 101)):
            raise forms.ValidationError("Ставка должна быть от 0 до 100%")
        return rate
