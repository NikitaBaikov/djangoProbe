from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<transaction_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<transaction_id>[0-9]+)/edit/$', views.edit, name='edit'),
	url(r'^new/$', views.new_transaction, name='new_transaction'),
] 

