from django import forms
from .models import Category

class NewListing(forms.Form):
	title = forms.CharField(label="Title", required=True)
	description = forms.CharField(label="Description", widget=forms.Textarea, required=False)
	price = forms.FloatField(label="Starting Price", required=True)
	img_url = forms.URLField(label="Image URL (optional)", required=False)
	category = forms.ChoiceField(choices=[(i, str(obj)) for i, obj in enumerate(Category.objects.all())], label="Category")