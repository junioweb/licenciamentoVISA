# -*- encoding: utf-8 -*-

from django.forms import ModelForm, Select, SelectMultiple, TextInput
from django import forms
from segCadastro.models import Processo, Pessoa_Fisica, Pessoa_Juridica, Processo_Tramita_Setor
from segCadastro.models import Estabelecimento_Desempenha_Atv, Responsavel, Equipamento_Saude
from segCadastro.models import Autorizacao_Funcionamento, Veiculo

class ProcessoForm(ModelForm):
    class Meta:
        model = Processo
        exclude = ['TramitaSetor', 'ProcessoMae', 'Estabelecimento']
        widgets = {
            'Tipo': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Assunto': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Atividade_Estabelecimento': SelectMultiple(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Setor': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
        }

class PessoaFisicaForm(ModelForm):
    class Meta:
        model = Pessoa_Fisica
        exclude = ['Atividade']
        widgets = {
            'Municipio': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
        }

class PessoaJuridicaForm(ModelForm):
    class Meta:
        model = Pessoa_Juridica
        exclude = ['Atividade']
        widgets = {
            'NaturezaJuridica': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Situacao': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Municipio': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'EstabelecimentoMantenedor': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'ProfissionaisCCIH': SelectMultiple(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'ResponsaveisLegais': SelectMultiple(attrs={'class': 'js-example-basic-single js-states form-control'}),
        }

class EstabelecimentoDesempenhaAtvForm(ModelForm):
    class Meta:
        model = Estabelecimento_Desempenha_Atv
        exclude = ['Estabelecimento', 'Atividade']
        widgets = {
            'ResponsavelTecnico': SelectMultiple(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Veiculo': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
        }

class TramitaSetorForm(ModelForm):
    class Meta:
        model = Processo_Tramita_Setor
        exclude = ['Processo']
        widgets = {
            'Setor': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Operacao': Select(attrs={'class': 'form-control'}),
        }

class ResponsavelForm(ModelForm):
    class Meta:
        model = Responsavel
        exclude = ['']
        widgets = {
            'Municipio': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'CBO': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
        }

class EquipamentoSaudeForm(ModelForm):
    class Meta:
        model = Equipamento_Saude
        exclude = ['Estabelecimento']

class AutorizacaoFuncionamentoForm(ModelForm):
    class Meta:
        model = Autorizacao_Funcionamento
        exclude = ['PessoaJuridica']

class VeiculoForm(ModelForm):
    class Meta:
        model = Veiculo
        exclude = ['']
