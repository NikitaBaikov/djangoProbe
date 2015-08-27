from django.contrib import admin

from .models import Transaction, Object

class ObjectInline (admin.TabularInline):
	model = Object
	extra = 3
	verbose_name_plural = 'Товары'

class TransactionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None , {'fields' : ['tr_name']}),
		(None , {'fields' : ['pub_date']})
	]
	inlines = [ObjectInline]

admin.site.register(Transaction, TransactionAdmin)

