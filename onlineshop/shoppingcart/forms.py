
from django import forms
class CartAddProductForm(forms.Form):
	units = forms.IntegerField( label="Quantity", help_text="Quantity:", required=True);
	update_units = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False )
	
	def clean(self):
		cleaned_data = self.cleaned_data
		cleaned_data['units'] = cleaned_data.get('units')
		cleaned_data['update'] = cleaned_data.get('update_units')

	#def __init__(self, *args, **kwargs):
	#	stock = kwargs.pop('stock', False)
	#	super(CartAddProductForm, self).__init__(*args, **kwargs)
	#	self.fields['units'].choices = [(i, i) for i in range(0, stock+1)]
