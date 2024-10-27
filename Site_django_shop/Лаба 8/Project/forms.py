from django import forms

class SliderForm(forms.Form):
    LowBlue = forms.IntegerField(min_value=-1, max_value=1000000, initial=-1)
    UpBlue = forms.IntegerField(min_value=-1, max_value=1000000, initial=0)

    LowGreen = forms.IntegerField(min_value=-1, max_value=1000000, initial=1)
    UpGreen = forms.IntegerField(min_value=-1, max_value=1000000, initial=10)

    LowOrange = forms.IntegerField(min_value=-1, max_value=1000000, initial=11)
    UpOrange = forms.IntegerField(min_value=-1, max_value=1000000, initial=12)

    LowRed = forms.IntegerField(min_value=-1, max_value=1000000, initial=13)
    UpRed = forms.IntegerField(min_value=-1, max_value=1000000, initial=1000000)

    even_number = forms.IntegerField(required=False, label='Проверить на кратность')