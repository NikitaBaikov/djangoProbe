from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Transaction
from .forms import ObjectForm

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
		raise Http404("Искомой сделки не существует")

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
		raise Http404("Искомой сделки не существует")

	if request.method == "POST":
		forms = [ObjectForm(prefix=obj.id, data=request.POST, instance=obj) for obj in tr.object_set.all()]
		ok = True
		for form in forms:
			if form.is_valid():
				form.save()
			else:
				ok = False
		if ok:
			return redirect('transactions:detail', transaction_id=transaction_id)

	template = loader.get_template('transactions/edit.html')
	forms = [ObjectForm(prefix=obj.id, instance=obj) for obj in tr.object_set.all()]

	context = RequestContext(request, {
		'tr': tr,
		'transaction_id': transaction_id,
		'forms' : forms,
	})

	return HttpResponse(template.render(context))


def save (request, transaction_id):
	tr = get_object_or_404(Transactions, pk=transaction_id)
	try:
		render (request, 'transactions/detail.html', {
			'tr' : tr,
			'transaction_id': transaction_id,
		})

	except (KeyError, Object.DoesNotExist):
		render (request, 'transactions/edit.html', {
			'tr' : tr,
			'transaction_id': transaction_id,
			'error_message' : "Ошибка при обработке формы"
		})






