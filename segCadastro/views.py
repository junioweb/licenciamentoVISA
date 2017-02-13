# -*- encoding: utf-8 -*-

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import A4
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import os, re, json
from django.forms.formsets import formset_factory, BaseFormSet
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

from segCadastro.models import Processo, Estabelecimento, Pessoa_Fisica, Pessoa_Juridica
from segCadastro.models import Estabelecimento_Desempenha_Atv, Atividade, Processo_Tramita_Setor
from segCadastro.models import Responsavel, Documento

from segCadastro.printing import MyPrint
from django.core.validators import EMPTY_VALUES

from segCadastro.forms import ProcessoForm, PessoaFisicaForm, PessoaJuridicaForm, VeiculoForm
from segCadastro.forms import TramitaSetorForm, EstabelecimentoDesempenhaAtvForm, DocumentoForm
from segCadastro.forms import ResponsavelForm, EquipamentoSaudeForm, AutorizacaoFuncionamentoForm
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.exceptions import PermissionDenied, MultipleObjectsReturned, ValidationError

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

@login_required
@permission_required('segCadastro.emitir_alvara', raise_exception=True)
def emitir_alvara(request, usuario, processo, obs):
    documentos = Documento.objects.filter(Processo__pk=processo.Numero)
    for documento in documentos:
        if documento.Assunto == u'AUTORIZAÇÃO DE FUNCIONAMENTO (AGEVISA)':
            raise MultipleObjectsReturned("Alvará já foi Emitido.")

    buffer = BytesIO()
    report = MyPrint(buffer, 'A4')

    descricao = "Autorização de Funcionamento referente ao Exercício: "+str(processo.Exercicio)+"."
    doc = Documento(Publico=True, Assunto='AUTORIZAÇÃO DE FUNCIONAMENTO (AGEVISA)', Descricao=descricao, Usuario=usuario, Processo=processo)
    doc.save()

    pdf = report.alvara(processo, doc.CodAutenticidade, usuario, obs)
    arquivo = ContentFile(pdf)
    filename = "Alvara-"+unicode(processo.Exercicio)+".pdf"
    doc.Arquivo.save(filename, arquivo)

@login_required
def home(request):
	return render(request, 'index.html',
							{'full_name': request.user.first_name, 'username':request.user.username})

def manutencao(request):
    return HttpResponse("Aguarde um momento, estamos em manutenção.")

def example(request):
	return render(request, 'example.html')

def consulta_geral(request):
    value = request.GET['value']
    data = {}
    errors = []

    try:
        if value in EMPTY_VALUES:
            raise ValueError("Nenhum valor foi informado.")
    except ValueError as e:
        data['errors'] = e
        return render(request, 'p_juridica_detalhes.html', data)

    if not value.isdigit():
        if not value[0].isdigit():
            numero = value[2:-11]

            try:
                data['processo'] = Processo.objects.get(pk=numero)
                data['lista_tramitacao'] = Processo_Tramita_Setor.objects.filter(Processo__pk=numero)
                data['lista_documentos'] = Documento.objects.filter(Processo__pk=numero)
                return render(request, 'p_juridica_detalhes.html', data)
            except Processo.DoesNotExist as e:
                errors.append('Processo não existe.')
                data['errors'] = errors
                return render(request, 'p_juridica_detalhes.html', data)
            except ValueError as e:
                errors.append("O valor informado é inválido: " + str(e))
                data['errors'] = errors
                return render(request, 'p_juridica_detalhes.html', data)
        else:
            value = re.sub("[-/\.]", "", value)

    try:
        int(value)
    except ValueError:
        errors.append('O valor informado é inválido.')
        data['errors'] = errors
        return render(request, 'p_juridica_detalhes.html', data)

    if len(value) == 14 or len(value) == 11:
        def DV_maker(v):
            if v >= 2:
                return 11 - v
            return 0

        if len(value) == 14:
            orig_dv = value[-2:]

            new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(5, 1, -1) + range(9, 1, -1))])
            new_1dv = DV_maker(new_1dv % 11)
            value = value[:-2] + str(new_1dv) + value[-1]
            new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(6, 1, -1) + range(9, 1, -1))])
            new_2dv = DV_maker(new_2dv % 11)
            value = value[:-1] + str(new_2dv)

            if value[-2:] != orig_dv:
                errors.append("O CNPJ é inválido.")
                data['errors'] = errors
                return render(request, 'p_juridica_detalhes.html', data)

            try:
                data['p_juridica'] = Pessoa_Juridica.objects.get(CNPJ=value)
                data['lista_processos'] = Processo.objects.filter(Estabelecimento__pk=data['p_juridica'].pk)
                data['lista_resp_legais'] = data['p_juridica'].ResponsaveisLegais.all()
                data['lista_atividades'] = data['p_juridica'].Atividade.all()
                data['lista_desempenha'] = Estabelecimento_Desempenha_Atv.objects.filter(Estabelecimento__pk=data['p_juridica'].pk)
                data['zipped_data'] = zip(data['lista_atividades'], data['lista_desempenha'])

                return render(request, 'p_juridica_detalhes.html', data)
            except Pessoa_Juridica.DoesNotExist:
                errors.append("Estabelecimento - Pessoa Jurídica não está cadastrada.")
            	data['errors'] = errors
                return render(request, 'p_juridica_detalhes.html', data)


        elif len(value) == 11:
            orig_dv = value[-2:]

            new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
            new_1dv = DV_maker(new_1dv % 11)
            value = value[:-2] + str(new_1dv) + value[-1]
            new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
            new_2dv = DV_maker(new_2dv % 11)
            value = value[:-1] + str(new_2dv)

            if value[-2:] != orig_dv:
                errors.append("O CPF é inválido.")
                data['errors'] = errors
                return render(request, 'p_juridica_detalhes.html', data)

            try:
                data['p_fisica'] = Pessoa_Fisica.objects.get(CPF=value)
                data['lista_processos'] = Processo.objects.filter(Estabelecimento__pk=data['p_fisica'].pk)
                data['lista_atividades'] = data['p_fisica'].Atividade.all()
                data['lista_desempenha'] = Estabelecimento_Desempenha_Atv.objects.filter(Estabelecimento__pk=data['p_fisica'].pk)
                data['zipped_data'] = zip(data['lista_atividades'], data['lista_desempenha'])

                return render(request, 'p_fisica_detalhes.html', data)
            except Pessoa_Fisica.DoesNotExist:
                errors.append("Estabelecimento - Pessoa Física não está cadastrada.")
                data['errors'] = errors
                return render(request, 'p_fisica_detalhes.html', data)

    else:
        errors.append("O valor requer 11 dígitos para CPF ou 14 dígitos para CNPJ.")
    	data['errors'] = errors
        return render(request, 'p_juridica_detalhes.html', data)

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
    try:
        form = ProcessoForm(request.POST or None)
        data = {}
        errors = []
        successes = []

        if form.is_valid():
            processo = form.save(commit=False)
            processos = Processo.objects.filter(Estabelecimento_id=request.POST.get('estabelecimento_id'))
            
            for value in processos:
                if value.Assunto_id == 18:                
                    situacoes = Processo_Tramita_Setor.objects.filter(Processo_id=value.pk).order_by('-Situacao')[:1]
                    for situacao in situacoes:
                        if situacao.Situacao == 'PENA_APL' and request.POST.get('Assunto') != '18':
                            raise ValidationError('Processo não pôde ser gerado. Pois existe uma penalidade aplicada ao regulado.')

            if request.POST.get("processo_id"):
                processo.ProcessoMae = Processo.objects.get(pk=request.POST.get("processo_id"))
            if request.POST.get("estabelecimento_id"):
                processo.Estabelecimento = Estabelecimento.objects.get(pk=request.POST.get("estabelecimento_id"))
            
            successes.append("Processo criado com sucesso.", p_imprimir(request, request.POST.get("processo_id")))
            processo.save()

            data['successes'] = successes
            return render(request, 'resultado.html', data)

        return render(request, 'processo_create.html', {'form':form})
    except ValidationError as e:
        data['errors'] = e
        return render(request, 'resultado.html', data)
    except Exception as e:
        data['errors'] = e
        return render(request, 'resultado.html', data)

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
def veiculo_create(request):
    form = VeiculoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'veiculo_create.html', {'form':form})

@login_required
def documento_include(request):
    form = DocumentoForm(request.POST or None, request.FILES or None)
    data = {}
    errors = []
    successes = []

    if request.method == 'POST':
        if form.is_valid():
            try:
                documento = form.save(commit=False)
                documento.Usuario = request.user
                documento.Processo = Processo.objects.get(pk=request.POST.get("processo_id"))

                successes.append("Documento inserido com sucesso")
                documento.save()
                data['successes'] = successes
            except UnicodeDecodeError as e:
                data['errors'] = e
            except OSError as e:
                data['errors'] = e
            except Exception as e:
                data['errors'] = e

            return render(request, 'resultado.html', data)

    return render(request, 'documento_include.html', {'form':form})

@login_required
def estab_atv_vincular(request):
    form = EstabelecimentoDesempenhaAtvForm(request.POST or None)

    if form.is_valid():
        vincular = form.save(commit=False)
        vincular.Estabelecimento = Estabelecimento.objects.get(pk=request.POST.get("estabelecimento_id"))
        vincular.Atividade = Atividade.objects.get(pk=request.POST.get("atividade_id"))
        vincular.save()
        return redirect('p_juridica_listar')

    return render(request, 'estab_atv_vincular.html', {'object':estabelecimento, 'form':form})

@login_required
def processo_reorientar(request):
    form = TramitaSetorForm(request.POST or None)
    data = {}
    errors = []
    successes = []

    if form.is_valid():
        try:
            tramitacao = form.save(commit=False)
            tramitacao.Usuario = request.user
            tramitacao.Processo = Processo.objects.get(pk=request.POST.get("processo_id"))

            if tramitacao.Situacao == 'DEF' and tramitacao.Alvara == True:
                try:
                    emitir_alvara(request, tramitacao.Usuario, tramitacao.Processo, tramitacao.Obs)
                except PermissionDenied as e:
                    raise e

                successes.append("Alvará emitido com sucesso")
            tramitacao.save()
            successes.append("Tramitação realizada com sucesso")
            data['successes'] = successes
        except MultipleObjectsReturned as e:
            data['errors'] = e
        except UnicodeDecodeError as e:
            data['errors'] = e
        except OSError as e:
            data['errors'] = e
        except Exception as e:
            raise e

        return render(request, 'resultado.html', data)

    return render(request, 'processo_reorientar.html', {'form':form})

def busca_autocomplete_processo(request):
    busca = request.GET.get("term")
    processos = Processo.objects.filter(Numero__istartswith=busca)
    res = [ dict(name=p.__unicode__(), id=p.pk,) for p in processos ]

    return HttpResponse(json.dumps(res),)

def busca_autocomplete_estabelecimento(request):
    busca = request.GET.get("term")
    estabelecimentosCPF = Pessoa_Fisica.objects.filter(CPF__istartswith=busca)
    estabelecimentosCNPJ = Pessoa_Juridica.objects.filter(CNPJ__istartswith=busca)

    res = [ dict(name=e.__unicode__(), id=e.pk,) for e in estabelecimentosCNPJ ]
    res2 = [ dict(name=e.__unicode__(), id=e.pk,) for e in estabelecimentosCPF ]

    return HttpResponse(json.dumps(res2+res))

def busca_autocomplete_atividade(request):
    busca = request.GET.get("term")
    atividades = Atividade.objects.filter(Subclasse__istartswith=busca)
    res = [ dict(name=a.__unicode__(), id=a.pk,) for a in atividades ]

    return HttpResponse(json.dumps(res),)

def busca_autocomplete_responsavel(request):
    busca = request.GET.get("term")
    responsaveis = Responsavel.objects.filter(CPF__istartswith=busca)
    res = [ dict(name=r.__unicode__(), id=r.pk,) for r in responsaveis ]

    return HttpResponse(json.dumps(res),)

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
    i = os.path.join('/servidorvps/sites/seg.agevisa.pb.gov.br/htdocs/static/img/topo-A4.jpg')
    p.setFont("Helvetica", 10)
    p.drawString(40, 820, unicode(timezone.localtime(timezone.now()).strftime("%d-%m-%Y %H:%M:%S")))
    p.drawImage(i, 0, 750, width=21.6*cm, height=2.2*cm)
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
        if hasattr(pessoa, 'RazaoSocial') and pessoa.EstabelecimentoMantenedor:
            p.setFont("Helvetica-Bold", 14)
            p.drawString(40, 340, 'Estabelecimento Mantenedor:')
            p.setFont("Helvetica", 10)
            p.drawString(40, 320, u"Razão Social: "+pessoa.EstabelecimentoMantenedor.RazaoSocial)
            p.drawString(40, 300, "CNPJ: "+pessoa.EstabelecimentoMantenedor.CNPJ)
            i = 280
        else:
            i = 340

        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, i, u'Caracterização da(s) Atividade(s) Econômica(s):')
        p.setFont("Helvetica", 9)

        for ar in estab_atividade:
            atividade = Atividade.objects.get(pk=ar.Atividade_id)
            i = i-20
            p.drawString(40, i, atividade.Subclasse+' - '+atividade.Denominacao)
            if ar.Veiculo:
                i = i-10
                p.drawString(40, i, unicode(ar.Veiculo))

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
