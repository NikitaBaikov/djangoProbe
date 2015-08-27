from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<transaction_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<transaction_id>[0-9]+)/edit/$', views.edit, name='edit'),
	url(r'^(?P<transaction_id>[0-9]+)/save/$', views.edit, name='save'),
] 

