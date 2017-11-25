
from django import forms

class CartAddProductForm(forms.Form):
	units = forms.IntegerField( label="Quantity", help_text="Select the number of items", required=True);
	update_units = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False )
	
	def clean(self):
		cleaned_data = self.cleaned_data
		cleaned_data['units'] = cleaned_data.get('units')
		cleaned_data['update'] = cleaned_data.get('update_units')
