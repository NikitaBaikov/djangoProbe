from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.forms.formsets import formset_factory
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse

from .models import Transaction
from .forms import TrObjectForm, TrForm, MyBaseFormSet

def index (request):
	if request.method == "GET":
		tr_event = request.GET.get('tr_event', '')	

		tr_list = Transaction.objects.order_by('-pub_date')
		
		# TODO Зафиксировать порядок вывода, но сохранить id		
		
		# Словари для всех сделок (включая id)
		tr_list_info =[model_to_dict(obj) for obj in tr_list]
	
		# Словарь для шапки таблицы
		labels = { k : Transaction._meta.get_field(k).verbose_name for k in 
			[getattr(field, 'name') for field in Transaction._meta.fields]
		}

		template = loader.get_template('transactions/index.html')
		context = RequestContext(request, {
			'tr_event' : tr_event,
			'tr_list_info' : tr_list_info,
			'labels' : labels,
		})
		return HttpResponse(template.render(context))

def delete (request, transaction_id):
	try:
		tr = Transaction.objects.get(pk=transaction_id)
	except Transaction.DoesNotExist:
		raise Http404
	
	tr.delete()
	
	# В случае успешной обработки выводим сообщение об удалении
	return HttpResponseRedirect(reverse('transactions:index') + '?tr_event=delete')


def detail (request, transaction_id):
	try:
		tr = Transaction.objects.get(pk=transaction_id)
	except Transaction.DoesNotExist:
		raise Http404

	if request.method == "GET":
		tr_event = request.GET.get('tr_event', '')	

		template = loader.get_template('transactions/detail.html')

		# У формы имеется порядок отображения полей, поэтому воспользуемся ей, а не словарем
		tr_info = TrForm(data=model_to_dict(tr))
		tr_objects_info = [TrObjectForm(data = model_to_dict(obj)) for obj in tr.trobject_set.all()]
		context = RequestContext(request, {
			'tr_event' : tr_event,
			'tr_info': tr_info,
			'tr_objects_info': tr_objects_info,
			'transaction_id': transaction_id,
		})

		return HttpResponse(template.render(context))


def edit (request, transaction_id):
	try:
		tr = Transaction.objects.get(pk=transaction_id)
	except Transaction.DoesNotExist:
		raise Http404

	TrObjectFormSet = formset_factory(TrObjectForm, formset=MyBaseFormSet, extra=0)
	
	# Обработка формы	
	if request.method == 'POST':	

		# Прикрепляемся у уже существующей сделке
		myTrForm = TrForm(request.POST, instance=tr)

		myFormset = TrObjectFormSet(request.POST)

		# TODO has_changed() всегда true? 
		print ([form.has_changed() for form in myFormset])	
	
		if myFormset.is_valid() and myTrForm.is_valid():
			tr_instance = myTrForm.save()

			# Удаляем все старые товары
			tr.trobject_set.all().delete()

			#  Надо прикрепить товары
			for form in myFormset:
				# Данные неполны, нужен еще ключ на саму сделку. Поэтому commit = False
				instance = form.save(commit = False)
				
				# Вручную прикрепляем к нашей сделке товары из формы
				tr_instance.trobject_set.add(instance)
	
			# В случае успешной обработки выводим сообщение об изменении
			return HttpResponseRedirect(reverse('transactions:detail', 
				kwargs = {'transaction_id' : transaction_id}) + '?tr_event=change')

		return HttpResponseRedirect(reverse('transactions:edit', 
			kwargs = {'transaction_id' : transaction_id}))

	else:
		# Переход на страницу с неотредактированной формой
		template = loader.get_template('transactions/edit.html')

		myTrForm = TrForm(initial = model_to_dict(tr))
		myFormset = TrObjectFormSet(initial = [model_to_dict(obj) for obj in tr.trobject_set.all()])

		context = RequestContext(request, {
			'myTrForm' : myTrForm,
			'myFormset' : myFormset
		})
		
		return HttpResponse(template.render(context))
	

def new_transaction (request):
	TrObjectFormSet = formset_factory(TrObjectForm, formset=MyBaseFormSet)

	# Обработка формы	
	if request.method == 'POST':	

		myTrForm = TrForm(request.POST)
		myFormset = TrObjectFormSet(request.POST)
		
		if myFormset.is_valid() and myTrForm.is_valid():
			tr_instance = myTrForm.save()
			
			#  Надо прикрепить товары
			for form in myFormset:
				# Данные неполны, нужен еще ключ на саму сделку. Поэтому commit = False
				instance = form.save(commit = False)

				# Вручную прикрепляем к нашей сделке
				tr_instance.trobject_set.add(instance)
	
			# В случае успешной обработки выводим сообщение об успехе
			return HttpResponseRedirect(reverse('transactions:index') + '?tr_event=add')

		return redirect('transactions:new_transaction')

	else:
		# Переход на страницу с пустой формой
		template = loader.get_template('transactions/new_transaction.html')

		myTrForm = TrForm()
		myFormset = TrObjectFormSet()

		context = RequestContext(request, {
			'myTrForm' : myTrForm,
			'myFormset' : myFormset
		})
		
		return HttpResponse(template.render(context))
