# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-01 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segCadastro', '0006_auto_20160331_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='processo_tramita_setor',
            name='Alvara',
            field=models.BooleanField(default=False, verbose_name=b'Alvar\xc3\xa1'),
        ),
    ]
