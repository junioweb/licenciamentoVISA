# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 09:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segCadastro', '0003_auto_20160328_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa_juridica',
            name='CNPJ',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True),
        ),
    ]
