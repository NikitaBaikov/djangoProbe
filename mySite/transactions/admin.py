from django.contrib import admin

from .models import Transaction, TrObject

class TrObjectInline (admin.TabularInline):
	model = TrObject
	extra = 3
	verbose_name_plural = 'Товары'

class TransactionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None , {'fields' : ['tr_name']}),
		(None , {'fields' : ['pub_date']})
	]
	inlines = [TrObjectInline]

admin.site.register(Transaction, TransactionAdmin)

