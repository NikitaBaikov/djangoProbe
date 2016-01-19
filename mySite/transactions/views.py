from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.forms.formsets import formset_factory

from .models import Transaction
from .forms import TrObjectForm

def index (request):
	tr_list = Transaction.objects.order_by('-pub_date')
	template = loader.get_template('transactions/index.html')
	context = RequestContext(request, {
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
	template = loader.get_template('transactions/new_transaction.html')

	TrObjectFormSet = formset_factory(TrObjectForm)
	myFormset = TrObjectFormSet()

	context = RequestContext(request, {
		'myFormset' : myFormset
	})

	return HttpResponse(template.render(context))

