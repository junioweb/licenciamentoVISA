# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segCadastro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa_juridica',
            name='CNPJ',
            field=models.CharField(blank=True, max_length=14),
        ),
    ]
