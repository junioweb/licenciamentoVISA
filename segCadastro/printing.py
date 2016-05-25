# -*- encoding: utf-8 -*-

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)
import os
from django.utils import timezone

class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    @staticmethod
    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Header
        header = Paragraph('ESTE DOCUMENTO DEVERÁ PERMANECER EXPOSTO EM LOCAL VISÍVEL', styles['centered'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('Emitido em: '+unicode(timezone.localtime(timezone.now()).strftime("%d-%m-%Y %H:%M:%S")), styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()

    def alvara(self, processo, codAutenticidade, usuario, obs):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch/1.7,
                                leftMargin=inch/1.6,
                                topMargin=inch/2,
                                bottomMargin=inch/4,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        styles2= {
            'default': ParagraphStyle(
                'default',
                fontName='Helvetica',
                fontSize=10,
                leading=12,
                leftIndent=0,
                rightIndent=0,
                firstLineIndent=0,
                alignment=TA_JUSTIFY,
                spaceBefore=6,
                spaceAfter=0,
                bulletFontName='Helvetica',
                bulletFontSize=10,
                bulletIndent=0,
                textColor= black,
                backColor=None,
                wordWrap=None,
                borderWidth= 0,
                borderPadding= 0,
                borderColor= None,
                borderRadius= None,
                allowWidows= 1,
                allowOrphans= 0,
                textTransform=None,  # 'uppercase' | 'lowercase' | None
                endDots=None,
                splitLongWords=1,
            ),
        }
        styles2['title'] = ParagraphStyle(
            'title',
            parent=styles2['default'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=42,
            spaceBefore=10,
            alignment=TA_CENTER,
            textColor=black,
        )
        styles2['bold'] = ParagraphStyle(
            'bold',
            parent=styles2['default'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            spaceBefore=10,
            alignment=TA_JUSTIFY,
            textColor=black,
        )
        styles2['assinatura'] = ParagraphStyle(
            'assinatura',
            parent=styles2['default'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=10,
            spaceBefore=10,
            alignment=TA_CENTER,
            textColor=black,
        )
        styles2['abaixoAssinatura'] = ParagraphStyle(
            'abaixoAssinatura',
            parent=styles2['default'],
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            spaceBefore=12,
            alignment=TA_CENTER,
            textColor=black,
        )

        if processo.ProcessoMae == None:
            processoMae = 0
        else:
            processoMae = 1

        estabelecimento = processo.Estabelecimento
        empresa = estabelecimento.child_object()
        if hasattr(empresa, 'Nome'):
            nomeEmpresa = empresa.Nome
        elif hasattr(empresa, 'RazaoSocial'):
	        nomeEmpresa = empresa.RazaoSocial

        data = [['Exercício: '+str(processo.Exercicio)+' | Válido até: 31/03/'+str(int(processo.Exercicio)+1)],]
        t=Table(data)
        t.setStyle(TableStyle([#('GRID',(1,1),(-2,-2),1,(0,0,0)),
                                ('BOX',(0,0),(-1,-1),2,(0,0,0)),
                                ('ALIGN',(0,0),(0,0),'LEFT'),
                              ]))

        data = []
        data.append([Paragraph('Atividade(s) Econômica(s) (CNAE):', styles2['bold'])])
        #atividades = empresa.Atividade.all()
        atividades = processo.Atividade_Estabelecimento.all()
        for atividade in atividades:
            if hasattr(empresa, 'RazaoSocial'):
                if atividade.MedControlados and atividade.Atividade.Subclasse == '4771701' or atividade.MedControlados and atividade.Atividade.Subclasse == '4771703':
                    obs = 'APTA A DISPENSAR MEDICAMENTOS CONTROLADOS DA PORTARIA 344/98'
            data.append([Paragraph(unicode(atividade.Atividade), styles2['default'])])
            if atividade.Veiculo:
                data.append([Paragraph(unicode(atividade.Veiculo), styles2['bold'])])
            if hasattr(empresa, 'Nome'):
                data.append(['Responsável Técnico:'])
                data.append([unicode(empresa.Nome)+' - '+unicode(empresa.SiglaConselhoClasse)+'('+unicode(empresa.InscricaoConselhoClasse)+')'])
            elif hasattr(empresa, 'RazaoSocial'):
                data.append(['Responsável(eis) Técnico(s):'])
                resp_tecnicos = atividade.ResponsavelTecnico.all()
                for resp_tecnico in resp_tecnicos:
                    data.append([unicode(resp_tecnico.Nome)+' - '+unicode(resp_tecnico.SiglaConselhoClasse)+'('+unicode(resp_tecnico.InscricaoConselhoClasse)+')'])

        if obs:
            data.append([Paragraph('Observação:', styles2['bold'])])
            data.append([Paragraph(unicode(obs), styles2['default'])])

        t2=Table(data, doc.width)
        t2.setStyle(TableStyle([#('GRID',(1,1),(-2,-2),1,(0,0,0)),
                                ('BOX',(0,0),(-1,-1),1,(0,0,0)),
                                #('ALIGN',(0,0),(0,0),'LEFT'),
                              ]))

        texto = u'A Agência Estadual de Vigilância Sanitária através da '+unicode(processo.Setor.Nome)+' concede ao estabelecimento '+unicode(nomeEmpresa)+u' a presente Autorização de Funcionamento de acordo com as disposições da Lei nº 7069 de 12 de abril de 2002, Art. 4º, VI.'
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        I = Image(os.path.join(BASE_DIR, 'segCadastro/static/img/cabecalhoAlvara.jpg'))
        elements.append(I)
        elements.append(Paragraph('Autorização de Funcionamento', styles2['title']))
        elements.append(t)
        elements.append(Paragraph('Processo nº: '+str(processo.Tipo)+'-'+str(processo.Numero)+str(processo.Ano)+'.'+str(processo.Exercicio)+'.'+str(processoMae), styles2['default']))
        elements.append(Paragraph( texto, styles2['default']))
        elements.append(Paragraph('Número da Agevisa: '+str(estabelecimento.Pasta), styles2['default']))
        if hasattr(empresa, 'Nome'):
            elements.append(Paragraph('Nome: '+unicode(empresa.Nome), styles2['default']))
            elements.append(Paragraph('CPF: '+empresa.CPF, styles2['default']))
        elif hasattr(empresa, 'RazaoSocial'):
            elements.append(Paragraph(u'Razão Social: '+unicode(empresa.RazaoSocial), styles2['default']))
            if empresa.NomeFantasia:
                elements.append(Paragraph('Nome Fantasia: '+unicode(empresa.NomeFantasia)+', CNPJ: '+empresa.CNPJ, styles2['default']))
            else:
                elements.append(Paragraph('CNPJ: '+empresa.CNPJ, styles2['default']))
        elements.append(Paragraph(u'Município: '+unicode(estabelecimento.Municipio)+', CEP: '+estabelecimento.CEP, styles2['default']))
        elements.append(Paragraph(u'Endereço: '+estabelecimento.Endereco+', '+estabelecimento.Numero+' - '+estabelecimento.Bairro, styles2['default']))
        if hasattr(empresa, 'RazaoSocial'):
            elements.append(Paragraph(u'Resposável(eis) Legal(is): ', styles2['default']))
            resp_legais = empresa.ResponsaveisLegais.all()
            for resp_legal in resp_legais:
                elements.append(Paragraph(unicode(resp_legal), styles2['default']))
            if empresa.EstabelecimentoMantenedor:
                elements.append(Paragraph(u'Estabelecimento Mantenedor: ', styles2['bold']))
                elements.append(Paragraph(u'Razão Social: '+unicode(empresa.EstabelecimentoMantenedor.RazaoSocial), styles2['default']))
                if empresa.EstabelecimentoMantenedor.NomeFantasia:
                    elements.append(Paragraph('Nome Fantasia: '+unicode(empresa.EstabelecimentoMantenedor.NomeFantasia)+', CNPJ: '+empresa.EstabelecimentoMantenedor.CNPJ, styles2['default']))
                else:
                    elements.append(Paragraph('CNPJ: '+empresa.EstabelecimentoMantenedor.CNPJ, styles2['default']))

        elements.append(Paragraph('', styles2['default']))
        elements.append(t2)
        elements.append(Paragraph('', styles2['default']))
        elements.append(Paragraph(unicode(usuario.first_name)+" "+unicode(usuario.last_name), styles2['assinatura']))
        elements.append(Paragraph(unicode(processo.Setor.Nome), styles2['abaixoAssinatura']))
        elements.append(Paragraph('', styles2['default']))
        elements.append(Paragraph('', styles2['default']))
        elements.append(Paragraph('Todas as ações realizadas acima são por meio de Autenticação Eletrônica de Usuários', styles2['default']))
        elements.append(Paragraph('', styles2['default']))
        elements.append(Paragraph('Código de Autenticidade: '+str(codAutenticidade), styles2['default']))

        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer,
                  canvasmaker=NumberedCanvas)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(195 * mm, 1 * mm + (0.2 * inch),
                             "Página %d de %d" % (self._pageNumber, page_count))
