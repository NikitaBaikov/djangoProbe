from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.forms.formsets import formset_factory
from django.forms.models import model_to_dict

from .models import Transaction
from .forms import TrObjectForm, TrForm, MyBaseFormSet

def index (request, tr_event = ''):
	tr_list = Transaction.objects.order_by('-pub_date')
	template = loader.get_template('transactions/index.html')
	context = RequestContext(request, {
		'tr_event' : tr_event,
		'tr_list': tr_list,
	})
	return HttpResponse(template.render(context))

def detail (request, transaction_id):
	try:
		tr = Transaction.objects.get(pk=transaction_id)
	except Transaction.DoesNotExist:
		raise Http404

	template = loader.get_template('transactions/detail.html')

	tr_info = TrForm(data=model_to_dict(tr))
	print (tr.trobject_set.all())
	tr_objects_info = [TrObjectForm(data = model_to_dict(obj)) for obj in tr.trobject_set.all()]
	print (tr_objects_info)
	context = RequestContext(request, {
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

	if request.method == "POST":
		forms = [TrObjectForm(prefix=obj.id, data=request.POST, instance=obj) for obj in tr.object_set.all()]

		ok = True
		for form in forms:
			if form.is_valid():
				form.save()
			else:
				ok = False
		if ok:
			return redirect('transactions:detail', transaction_id=transaction_id)

	template = loader.get_template('transactions/edit.html')
	forms = [TrObjectForm(prefix=obj.id, instance=obj) for obj in tr.object_set.all()]
	
	context = RequestContext(request, {
		'tr': tr,
		'transaction_id': transaction_id,
		'forms' : forms,
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
			return redirect('transactions:index', tr_event = '#add')

		return redirect('transactions:index')

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
