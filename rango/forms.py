from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Category

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Enter title")
	url = forms.URLField(max_length=200, help_text="Enter url")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Page
		fields = ('title', 'url', 'views')