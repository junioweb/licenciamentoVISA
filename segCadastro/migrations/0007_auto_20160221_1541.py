# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('segCadastro', '0006_auto_20160221_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autorizacao_funcionamento',
            name='Estabelecimento',
        ),
        migrations.AddField(
            model_name='autorizacao_funcionamento',
            name='PessoaJuridica',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='segCadastro.Pessoa_Juridica'),
        ),
        migrations.AlterField(
            model_name='equipamento_saude',
            name='Caracteristicas',
            field=models.TextField(blank=True, null=True, verbose_name=b'Caracter\xc3\xadsticas'),
        ),
        migrations.AlterField(
            model_name='equipamento_saude',
            name='Tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='segCadastro.Tipo_Equipamento_Saude'),
        ),
    ]