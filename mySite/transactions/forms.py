from django.forms import ModelForm
from .models import TrObject, Transaction
from datetimewidget.widgets import DateTimeWidget
from django.forms.formsets import BaseFormSet

class TrObjectForm(ModelForm):
	class Meta:
		model = TrObject
		fields = ['object_name', 'number', 'price']

	# Добавим к полям класс form-control (нужен для bootstrap)
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

class TrForm(ModelForm):
	class Meta:
		model = Transaction
		fields = ['tr_name', 'pub_date']
		widgets = {'pub_date': DateTimeWidget(attrs={'id':'datetime_id'}, usel10n=True, bootstrap_version=3)}

	def __init__(self, *args, **kwargs):
		
		# Добавим к полям класс form-control (нужен для bootstrap)
		super(ModelForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

# Пустая форма в formset не будет считаться правильной
class MyBaseFormSet(BaseFormSet):
	def __init__(self, *args, **kwargs):
		super(MyBaseFormSet, self).__init__(*args, **kwargs)
		for form in self.forms:
			form.empty_permitted = False

