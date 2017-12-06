
from django import forms
from placeorder.models import Order

class OrderCreateForm(forms.Form):
	firstName = forms.CharField(label="First name:", help_text="Please enter your first name", required=True)
	familyName = forms.CharField(label="Last name:", help_text="Please enter your family name", required=True)
	email = forms.EmailField(label="Email:", help_text="Please enter your email", required=True)
	address = forms.CharField(label="Address:", help_text="Please enter your address", required=True)
	zip = forms.CharField(label="Postal code:", help_text="Please enter your postal code", required=True)
	city = forms.CharField(label="City:", help_text="Please enter your city", required=True)
	
	def save(self):
		data = self.cleaned_data
		order = Order(firstName = data['firstName'], familyName = data['familyName'], email = data['email'], address = data['address'], zip = data['zip'], city = data['city'])
		order.save()
		return order
		
