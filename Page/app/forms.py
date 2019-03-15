from django import forms


class SearchForm(forms.Form):
    question = forms.CharField(max_length=500, label="")
