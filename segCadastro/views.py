# -*- encoding: utf-8 -*-

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import A4
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import os
from django.forms.formsets import formset_factory, BaseFormSet

from segCadastro.models import Processo, Estabelecimento, Pessoa_Fisica, Pessoa_Juridica
from segCadastro.models import Estabelecimento_Desempenha_Atv, Atividade, Processo_Tramita_Setor
from segCadastro.models import Responsavel

from segCadastro.forms import ProcessoForm, PessoaFisicaForm, PessoaJuridicaForm
from segCadastro.forms import TramitaSetorForm, EstabelecimentoDesempenhaAtvForm
from segCadastro.forms import ResponsavelForm, EquipamentoSaudeForm, AutorizacaoFuncionamentoForm

def home(request):
	return render(request, 'index.html')

def example(request):
	return render(request, 'example.html')

def estabelecimento(request):
	return render(request, 'estabelecimento.html')

def processo_listar(request):
	data = {}
	data['lista_processos'] = Processo.objects.all()
	return render(request, 'processo_listar.html', data)

def responsavel_listar(request):
	data = {}
	data['lista_responsaveis'] = Responsavel.objects.all()
	return render(request, 'responsavel_listar.html', data)

def p_fisica_listar(request):
	data = {}
	data['lista_p_fisica'] = Pessoa_Fisica.objects.all()
	return render(request, 'p_fisica_listar.html', data)

def p_juridica_listar(request):
	data = {}
	data['lista_p_juridica'] = Pessoa_Juridica.objects.all()
	return render(request, 'p_juridica_listar.html', data)

def p_fisica_editar(request, pk):
    p_fisica = Pessoa_Fisica.objects.get(pk=pk)

    form = PessoaFisicaForm(request.POST or None, instance=p_fisica)

    if form.is_valid():
        form.save()
        return redirect('p_fisica_listar')

    return render(request, 'p_fisica_editar.html', {'object':p_fisica, 'form':form})

def p_juridica_editar(request, pk):
    p_juridica = Pessoa_Juridica.objects.get(pk=pk)

    form = PessoaJuridicaForm(request.POST or None, instance=p_juridica)

    if form.is_valid():
        form.save()
        return redirect('p_juridica_listar')

    return render(request, 'p_juridica_editar.html', {'object':p_juridica, 'form':form})

def responsavel_editar(request, pk):
    responsavel = Responsavel.objects.get(pk=pk)

    form = ResponsavelForm(request.POST or None, instance=responsavel)

    if form.is_valid():
        form.save()
        return redirect('responsavel_listar')

    return render(request, 'responsavel_editar.html', {'object':responsavel, 'form':form})

def processo_create(request):
    form = ProcessoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('processo_listar')

    return render(request, 'processo_create.html', {'form':form})

def responsavel_create(request):
    form = ResponsavelForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('responsavel_listar')

    return render(request, 'responsavel_create.html', {'form':form})

def p_fisica_create(request):
    form = PessoaFisicaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('p_fisica_listar')

    return render(request, 'p_fisica_create.html', {'form':form})

def pessoa_juridica_create(request):
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False
    AtividadesFormSet = formset_factory(EstabelecimentoDesempenhaAtvForm, max_num=None, formset=RequiredFormSet)
    AfeFormSet = formset_factory(AutorizacaoFuncionamentoForm, max_num=None, formset=RequiredFormSet)
    EquipamentoFormSet = formset_factory(EquipamentoSaudeForm, max_num=None, formset=RequiredFormSet)

    formPessoaJuridica = PessoaJuridicaForm(None)
    atividade_formset = AtividadesFormSet(None)
    afe_formset = AfeFormSet(None)
    equipamento_formset = EquipamentoFormSet(None)

    if request.POST:
        atividade_formset = AtividadesFormSet(request.POST, request.FILES)
        formPessoaJuridica = PessoaJuridicaForm(request.POST)
        afe_formset = AfeFormSet(request.POST, request.FILES)
        equipamento_formset = EquipamentoFormSet(request.POST, request.FILES)

        if formPessoaJuridica.is_valid() and atividade_formset.is_valid and afe_formset.is_valid and equipamento_formset.is_valid:
            pessoaJuridica = formPessoaJuridica.save()

            for form in afe_formset.forms:
                autorizacao = form.save(commit=False)
                autorizacao.PessoaJuridica = pessoaJuridica
                autorizacao.save()
            for form in equipamento_formset.forms:
                equipamento = form.save(commit=False)
                equipamento.Estabelecimento = pessoaJuridica
                equipamento.save()
            for form in atividade_formset.forms:
                atividade = form.save(commit=False)
                atividade.Estabelecimento = pessoaJuridica
                atividade.save()

                '''
				atividade = form.cleaned_data.get('Atividade')
                manipular = form.cleaned_data.get('Manipular')
                fracionar = form.cleaned_data.get('Fracionar')
                dispensar = form.cleaned_data.get('Dispensar')
                aferirParam = form.cleaned_data.get('AferirParam')
                prestarAten = form.cleaned_data.get('PrestarAten')
                admAplicar = form.cleaned_data.get('AdmAplicar')
                perfurar = form.cleaned_data.get('Perfurar')
                dispRemoto = form.cleaned_data.get('DispRemoto')
                fabricar = form.cleaned_data.get('Fabricar')
                transformar = form.cleaned_data.get('Transformar')
                purificar = form.cleaned_data.get('Purificar')
                extrair = form.cleaned_data.get('Extrair')
                fragmentar = form.cleaned_data.get('Fragmentar')
                sintetizar = form.cleaned_data.get('Sintetizar')
                estRadiacaoIon = form.cleaned_data.get('EstRadiacaoIon')
                estETO = form.cleaned_data.get('EstETO')
                estOutras = form.cleaned_data.get('EstOutras')
                reprocessar = form.cleaned_data.get('Reprocessar')
                irradiar = form.cleaned_data.get('Irradiar')
                transportar = form.cleaned_data.get('Transportar')
                expedir = form.cleaned_data.get('Expedir')
                armazenar = form.cleaned_data.get('Armazenar')
                embalar = form.cleaned_data.get('Embalar')
                distribuir = form.cleaned_data.get('Distribuir')
                importar = form.cleaned_data.get('Importar')
                impUsoProprio = form.cleaned_data.get('ImpUsoProprio')
                exportar = form.cleaned_data.get('Exportar')
                realEtapFab = form.cleaned_data.get('RealEtapFab')
                responsavelForm = form.cleaned_data.get('ResponsavelTecnico')
                veiculo = form.cleaned_data.get('Veiculo')
                setor = form.cleaned_data.get('Setor')

                pj_atividade = Estabelecimento_Desempenha_Atv(Estabelecimento=pessoaJuridica,
															  Atividade=atividade,
															  Manipular=manipular,
															  Fracionar = fracionar,
											  				  Dispensar = dispensar,
											  				  AferirParam = aferirParam,
											  				  PrestarAten = prestarAten,
											  				  AdmAplicar = admAplicar,
											  			      Perfurar = perfurar,
											  			      DispRemoto = dispRemoto,
											  			      Fabricar = fabricar,
											  			      Transformar = transformar,
											  			      Purificar = purificar,
											  			      Extrair = extrair,
											  			      Fragmentar = fragmentar,
											  			      Sintetizar = sintetizar,
											  			      EstRadiacaoIon = estRadiacaoIon,
											  			      EstETO = estETO,
											  			      EstOutras = estOutras,
											  			      Reprocessar = reprocessar,
											  			      Irradiar = irradiar,
											  			      Transportar = transportar,
											  			      Expedir = expedir,
											  			      Armazenar = armazenar,
											  			      Embalar = embalar,
											  			      Distribuir = distribuir,
											  			      Importar = importar,
											  			      ImpUsoProprio = impUsoProprio,
											  			      Exportar = exportar,
											  			      RealEtapFab = realEtapFab,
															  Veiculo = veiculo,
															  Setor=setor,
															 )

                for responsavel in responsavelForm:
                    pj_atividade.save()
                    pj_atividade.ResponsavelTecnico.add(responsavel)
                    #import pdb; pdb.set_trace()
					'''


            return redirect('p_juridica_listar')

    c = {'formPessoaJuridica':formPessoaJuridica,
		 'atividade_formset':atividade_formset,
		 'afe_formset':afe_formset,
         'equipamento_formset':equipamento_formset,
	    }
    return render(request, 'pessoa_juridica_form.html', c)

def estab_atv_vincular(request):
    form = Estabelecimento_Desempenha_AtvForm(None)

    if request.POST:
        form = Estabelecimento_Desempenha_AtvForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('p_juridica_listar')

    return render(request, 'estab_atv_vincular.html', {'object':estabelecimento, 'form':form})

def processo_tramitar(request, pk):
    processo = Processo.objects.get(pk=pk)

    form = TramitaSetorForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('processo_listar')

    return render(request, 'processo_tramitar.html', {'object':processo, 'form':form})

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
    i = os.path.join('/servidorvps/sites/agevisa.tk/htdocs/static/img/topo-A4.jpg')
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
