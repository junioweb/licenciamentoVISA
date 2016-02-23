# -*- encoding: utf-8 -*-

from django.forms import ModelForm, Select, SelectMultiple
from segCadastro.models import Processo, Pessoa_Fisica, Pessoa_Juridica, Processo_Tramita_Setor
from segCadastro.models import Estabelecimento_Desempenha_Atv, Responsavel

class ProcessoForm(ModelForm):
    class Meta:
        model = Processo
        exclude = ['TramitaSetor']
        widgets = {
            'Tipo': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'ProcessoMae': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Estabelecimento': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Assunto': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Atividade_Estabelecimento': SelectMultiple(attrs={'class': 'js-example-basic-single js-states form-control'}),
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

class Estabelecimento_Desempenha_AtvForm(ModelForm):
    class Meta:
        model = Estabelecimento_Desempenha_Atv
        exclude = ['']
        widgets = {
            'Estabelecimento': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Atividade': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'ResponsavelTecnico': SelectMultiple(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Veiculo': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
            'Setor': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
        }

class TramitaSetorForm(ModelForm):
    class Meta:
        model = Processo_Tramita_Setor
        exclude = ['']
        widgets = {
            'Processo': Select(attrs={'class': 'js-example-basic-single js-states form-control'}),
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
