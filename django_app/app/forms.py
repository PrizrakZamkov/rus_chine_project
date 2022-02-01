from django import forms


class RusChineForm(forms.Form):
    rus = forms.CharField(label="Русский текст",  required=True, max_length=511,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    chine = forms.CharField(label="Китайский текст",  required=True, max_length=511,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
class WordWordForm(forms.Form):
    word_1 = forms.CharField(label="Original",  required=True, max_length=1023,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    word_2 = forms.CharField(label="Translate",  required=True, max_length=1023,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

class AddGroupForm(forms.Form):
    group = forms.CharField(label="Название группы",  required=True, max_length=51,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
