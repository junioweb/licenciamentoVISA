# -*- encoding: utf-8 -*-

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import A4
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import os
from django.forms.formsets import formset_factory, BaseFormSet
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

from segCadastro.models import Processo, Estabelecimento, Pessoa_Fisica, Pessoa_Juridica
from segCadastro.models import Estabelecimento_Desempenha_Atv, Atividade, Processo_Tramita_Setor
from segCadastro.models import Responsavel

from segCadastro.printing import MyPrint

from segCadastro.forms import ProcessoForm, PessoaFisicaForm, PessoaJuridicaForm
from segCadastro.forms import TramitaSetorForm, EstabelecimentoDesempenhaAtvForm
from segCadastro.forms import ResponsavelForm, EquipamentoSaudeForm, AutorizacaoFuncionamentoForm
from django.utils import timezone

def cadastrar_user(request):
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid(): # se o formulario for valido
            form.save() # cria um novo usuario a partir dos dados enviados
            return redirect("login") # redireciona para a tela de login
        else:
            # mostra novamente o formulario de cadastro com os erros do formulario atual
            return render(request, "cadastrar_user.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "cadastrar_user.html", {"form": UserCreationForm() })

def print_users(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    teste = "oooo.pdf"
    response['Content-Disposition'] = 'attachment; filename='+teste

    buffer = BytesIO()

    report = MyPrint(buffer, 'A4')
    pdf = report.print_users()

    response.write(pdf)
    return response

@login_required
def home(request):
	return render(request, 'index.html',
							{'full_name': request.user.first_name, 'username':request.user.username})

def example(request):
	return render(request, 'example.html')

@login_required
def consulta_geral(request):
    value = request.GET['value']

    if len(value) == 14:
        try:
            data = {}
            data['p_juridica'] = Pessoa_Juridica.objects.get(CNPJ=value)
            data['lista_processos'] = Processo.objects.filter(Estabelecimento__pk=data['p_juridica'].pk)
            data['lista_resp_legais'] = data['p_juridica'].ResponsaveisLegais.all()
            data['lista_atividades'] = data['p_juridica'].Atividade.all()
            data['lista_desempenha'] = Estabelecimento_Desempenha_Atv.objects.filter(Estabelecimento__pk=data['p_juridica'].pk)
            data['zipped_data'] = zip(data['lista_atividades'], data['lista_desempenha'])
        except Pessoa_Juridica.DoesNotExist:
            raise Http404("Estabelecimento - Pessoa Jurídica não existe!")
        return render(request, 'p_juridica_detalhes.html', data)
    return HttpResponse("Por favor, digite um CNPJ válido")

@login_required
def estabelecimento(request):
	return render(request, 'estabelecimento.html')

@login_required
def processo_listar(request):
	data = {}
	data['lista_processos'] = Processo.objects.all()
	return render(request, 'processo_listar.html', data)

@login_required
def responsavel_listar(request):
	data = {}
	data['lista_responsaveis'] = Responsavel.objects.all()
	return render(request, 'responsavel_listar.html', data)

@login_required
def p_fisica_listar(request):
	data = {}
	data['lista_p_fisica'] = Pessoa_Fisica.objects.all()
	return render(request, 'p_fisica_listar.html', data)

@login_required
def p_juridica_listar(request):
	data = {}
	data['lista_p_juridica'] = Pessoa_Juridica.objects.all()
	return render(request, 'p_juridica_listar.html', data)

@login_required
def p_fisica_editar(request, pk):
    p_fisica = Pessoa_Fisica.objects.get(pk=pk)

    form = PessoaFisicaForm(request.POST or None, instance=p_fisica)

    if form.is_valid():
        form.save()
        return redirect('p_fisica_listar')

    return render(request, 'p_fisica_editar.html', {'object':p_fisica, 'form':form})

@login_required
def p_juridica_editar(request, pk):
    p_juridica = Pessoa_Juridica.objects.get(pk=pk)

    form = PessoaJuridicaForm(request.POST or None, instance=p_juridica)

    if form.is_valid():
        form.save()
        return redirect('p_juridica_listar')

    return render(request, 'p_juridica_editar.html', {'object':p_juridica, 'form':form})

@login_required
def responsavel_editar(request, pk):
    responsavel = Responsavel.objects.get(pk=pk)

    form = ResponsavelForm(request.POST or None, instance=responsavel)

    if form.is_valid():
        form.save()
        return redirect('responsavel_listar')

    return render(request, 'responsavel_editar.html', {'object':responsavel, 'form':form})

@login_required
def processo_create(request):
    form = ProcessoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('processo_listar')

    return render(request, 'processo_create.html', {'form':form})

@login_required
def responsavel_create(request):
    form = ResponsavelForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('responsavel_listar')

    return render(request, 'responsavel_create.html', {'form':form})

@login_required
def p_fisica_create(request):
    form = PessoaFisicaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('p_fisica_listar')

    return render(request, 'p_fisica_create.html', {'form':form})

@login_required
def p_juridica_create(request):
    form = PessoaJuridicaForm(None)

    if request.POST:
        form = PessoaJuridicaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('p_juridica_listar')

    return render(request, 'p_juridica_create.html', {'form':form})

@login_required
def estab_atv_vincular(request):
    form = EstabelecimentoDesempenhaAtvForm(None)

    if request.POST:
        form = EstabelecimentoDesempenhaAtvForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('p_juridica_listar')

    return render(request, 'estab_atv_vincular.html', {'object':estabelecimento, 'form':form})

@login_required
def processo_tramitar(request, pk):
    processo = Processo.objects.get(pk=pk)

    form = TramitaSetorForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('processo_listar')

    return render(request, 'processo_tramitar.html', {'object':processo, 'form':form})

@login_required
def p_imprimir(request, pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="processo.pdf"'

    #processo_numero = request.GET
    buffer = BytesIO()
    processo = Processo.objects.get(pk=pk)
    tipo = processo.Tipo
    numero = processo.Numero
    ano = processo.Ano
    exercicio = processo.Exercicio
    estabelecimento = processo.Estabelecimento
    estab_atividade = processo.Atividade_Estabelecimento.all()
    processoMae = processo.ProcessoMae

    if processoMae != None:
		flagProcessoMae = 1
    else:
		flagProcessoMae = 0

    processo_numero = tipo+'-'+unicode(numero)+ano+'.'+exercicio+'.'+unicode(flagProcessoMae)

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #i = os.path.join('/servidorvps/sites/agevisa.tk/htdocs/static/img/topo-A4.jpg')
    p.setFont("Helvetica", 10)
    p.drawString(40, 820, str(timezone.now().strftime("%d-%m-%Y %H:%M:%S")))
    #p.drawImage(i, 0, 750, width=21.6*cm, height=2.2*cm)
    p.setFont("Helvetica", 14)
    p.drawCentredString(293, 730, u'GOVERNO DO ESTADO DA PARAÍBA')
    p.drawCentredString(293, 710, u'AGÊNCIA ESTADUAL DE VIGILÂNCIA SANITÁRIA')
    p.setFont("Helvetica-Bold", 24)
    p.drawString(40, 660, u'Processo nº: '+processo_numero)
    p.setFont("Helvetica", 10)
    p.drawString(40, 640, 'ASSUNTO: '+unicode(processo.Assunto))
    if processoMae != None:
		p.drawString(40, 620, u'Processo Mãe: '+unicode(processoMae))

    if estabelecimento != None:
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, 600, 'Dados do Estabelecimento:')
        p.setFont("Helvetica", 10)
        pessoa = estabelecimento.child_object()

        if hasattr(pessoa, 'Nome'):
            p.drawString(40, 580, "Nome: "+pessoa.Nome)
            p.drawString(40, 540, "CPF: "+pessoa.CPF)
        elif hasattr(pessoa, 'RazaoSocial'):
	        p.drawString(40, 580, u"Razão Social: "+pessoa.RazaoSocial)
	        p.drawString(40, 560, "Nome Fantasia: "+pessoa.NomeFantasia)
	        p.drawString(40, 540, "CNPJ: "+pessoa.CNPJ)

        p.drawString(40, 520, "CEP: "+estabelecimento.CEP)
        p.drawString(40, 500, u"Endereço: "+estabelecimento.Endereco)
        p.drawString(40, 480, u"Número: "+estabelecimento.Numero)
        p.drawString(40, 460, "Bairro: "+estabelecimento.Bairro)
        p.drawString(40, 440, u"Município: "+unicode(estabelecimento.Municipio))
        p.drawString(40, 420, u"Telefone Primário: "+unicode(estabelecimento.TelefonePrimario))
        if estabelecimento.TelefoneSecundario != 0:
            p.drawString(40, 400, u"Telefone Secundário: "+unicode(estabelecimento.TelefoneSecundario))
        p.drawString(40, 380, "E-mail: "+estabelecimento.Email)
        if processo.Obs != '':
            p.drawString(40, 360, u"Observação: "+processo.Obs)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, 320, u'Caracterização da(s) Atividade(s) Econômica(s):')
        p.setFont("Helvetica", 9)

        i = 320
        for ar in estab_atividade:
            atividade = Atividade.objects.get(pk=ar.Atividade_id)
            i = i-20
            p.drawString(40, i, atividade.Subclasse+' - '+atividade.Denominacao)

    else:
        if processo.Obs != '':
            p.drawString(40, 600, u"Observação: "+processo.Obs)

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
