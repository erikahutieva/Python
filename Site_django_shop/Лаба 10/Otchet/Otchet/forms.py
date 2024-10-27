from django import forms


class OrderForm(forms.Form):
    start_date = forms.DateField(
        label='Дата начала',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        label='Дата окончания',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )