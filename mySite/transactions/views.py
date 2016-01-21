from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.forms.formsets import formset_factory

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

	context = RequestContext(request, {
		'tr': tr,
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
	
	if request.method == 'POST':	

		myTrForm = TrForm(request.POST)
		myFormset = TrObjectFormSet(request.POST)
		
		if myFormset.is_valid() and myTrForm.is_valid():
			myTrForm.save()
			# TODO прикрепить товары
	
			return redirect('transactions:index', tr_event = '#add')

		return redirect('transactions:index')

	else:
		template = loader.get_template('transactions/new_transaction.html')

		myTrForm = TrForm()
		myFormset = TrObjectFormSet()

		context = RequestContext(request, {
			'myTrForm' : myTrForm,
			'myFormset' : myFormset
		})

		return HttpResponse(template.render(context))
