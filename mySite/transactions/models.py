from django.db import models

class Transaction(models.Model):
	tr_name = models.CharField('Сделка', max_length=200)
	pub_date = models.DateTimeField('Дата сделки')

	def __str__ (self):
		return self.tr_name


class TrObject(models.Model):
	tr = models.ForeignKey(Transaction)
	object_name = models.CharField('Товар', max_length=200)
	number = models.IntegerField('Количество', default=0)
	price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

