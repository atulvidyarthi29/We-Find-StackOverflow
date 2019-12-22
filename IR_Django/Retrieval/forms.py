from django import forms

class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=2000)
    search_tags = forms.CharField(max_length=2000)

