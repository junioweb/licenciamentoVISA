# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-13 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segCadastro', '0016_auto_20160920_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='estabelecimento_desempenha_atv',
            name='Base',
            field=models.BooleanField(default=False, verbose_name=b'Base do SAMU'),
        ),
    ]
