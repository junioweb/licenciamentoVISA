# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-01 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segCadastro', '0007_processo_tramita_setor_alvara'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documento',
            options={'ordering': ['DataHora']},
        ),
        migrations.AlterModelOptions(
            name='processo_tramita_setor',
            options={'ordering': ['DataHora'], 'verbose_name': 'Tramita\xe7\xe3o de Processo', 'verbose_name_plural': 'Tramita\xe7\xe3o de Processos'},
        ),
        migrations.AddField(
            model_name='estabelecimento_desempenha_atv',
            name='MedControlados',
            field=models.BooleanField(default=False, verbose_name=b'Medicamentos Controlados, Port. 344/98'),
        ),
    ]
