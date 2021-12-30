from django import forms


class RusChineForm(forms.Form):
    rus = forms.CharField(label="Русский текст",  required=True, max_length=511,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    chine = forms.CharField(label="Китайский текст",  required=True, max_length=511,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
