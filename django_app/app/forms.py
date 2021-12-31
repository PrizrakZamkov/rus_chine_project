from django import forms


class RusChineForm(forms.Form):
    rus = forms.CharField(label="Русский текст",  required=True, max_length=511,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    chine = forms.CharField(label="Китайский текст",  required=True, max_length=511,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

class AddGroupForm(forms.Form):
    group = forms.CharField(label="Название группы",  required=True, max_length=51,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

class RusToChi(forms.Form):
    text = forms.CharField(label="Русский --> Китайский", required=True, max_length=551,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
class ChiToRus(forms.Form):
    text = forms.CharField(label="Китайский --> Русский",  required=True, max_length=551,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
