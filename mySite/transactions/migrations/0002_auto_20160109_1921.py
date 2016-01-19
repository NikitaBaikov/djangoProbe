# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrObject',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('object_name', models.CharField(verbose_name='Товар', max_length=200)),
                ('number', models.IntegerField(verbose_name='Количество', default=0)),
                ('price', models.DecimalField(decimal_places=2, verbose_name='Цена', max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='object',
            name='tr',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tr_name',
            field=models.CharField(verbose_name='Сделка', max_length=200),
        ),
        migrations.DeleteModel(
            name='Object',
        ),
        migrations.AddField(
            model_name='trobject',
            name='tr',
            field=models.ForeignKey(to='transactions.Transaction'),
        ),
    ]
