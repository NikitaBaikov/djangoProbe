from django.forms import ModelForm
from .models import TrObject

class TrObjectForm(ModelForm):
	class Meta:
		model = TrObject
		fields = ['object_name', 'number', 'price']

	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'


