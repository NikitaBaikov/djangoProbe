# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('object_name', models.CharField(max_length=200)),
                ('number', models.IntegerField(default=0)),
                ('price', models.DecimalField(max_digits=20, decimal_places=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('tr_name', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='Дата сделки')),
            ],
        ),
        migrations.AddField(
            model_name='object',
            name='tr',
            field=models.ForeignKey(to='transactions.Transaction'),
        ),
    ]
