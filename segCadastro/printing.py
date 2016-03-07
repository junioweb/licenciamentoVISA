# -*- encoding: utf-8 -*-

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from django.contrib.auth.models import User
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
        footer = Paragraph('Emitido por: Fernando Júnior, em: '+str(timezone.now().strftime("%d-%m-%Y %H:%M:%S")), styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()

    def print_users(self):
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
                spaceBefore=10,
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

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        users = User.objects.all()

        data = [['Exercício: 2016 | Válido até: 31/03/2017'],]
        t=Table(data)
        t.setStyle(TableStyle([#('GRID',(1,1),(-2,-2),1,(0,0,0)),
                                ('BOX',(0,0),(-1,-1),2,(0,0,0)),
                                ('ALIGN',(0,0),(0,0),'LEFT'),
                              ]))

        data = [['Atividade(s) Econômica(s) (CNAE):'],
                ['8640-2/01 - LABORATÓRIOS DE ANATOMIA PATOLÓGICA E CITOLÓGICA'],
                ['Obs.: Distribuir, Armazenar, Importar, Exportar'],
                ['Responsável Técnico: JOSÉ AGRIPINO ARANTES - CRF: 1527'],
                [],
                ['8640-2/01 - LABORATÓRIOS DE ANATOMIA PATOLÓGICA E CITOLÓGICA'],
                ['Obs.: Placa: OEU-1524 - Tipo: B'],
                ['Responsável Técnico: JOSÉ AGRIPINO ARANTES - CRF: 1527'],
               ]
        t2=Table(data, doc.width)
        t2.setStyle(TableStyle([#('GRID',(1,1),(-2,-2),1,(0,0,0)),
                                ('BOX',(0,0),(-1,-1),1,(0,0,0)),
                                #('ALIGN',(0,0),(0,0),'LEFT'),
                              ]))

        data = [['Autorizo:', 'Conferido:', 'Visto:'],
                [Paragraph('Glaciane Mendes Roland', styles2['default']), Paragraph('Djanira Lucena de Araújo Machado', styles2['default']), Paragraph('Irlanilson Fabricio de Almeida', styles2['default'])],
                [Paragraph('DIRETORA GERAL - DG', styles2['default']), Paragraph('DIRETORA TÉCNICA DE MEDICAMENTOS, ALIMENTOS, PRODUTOS E TOXICOLOGIA - DTMAPT', styles2['default']), Paragraph('DIRETOR ADMINISTRATIVO FINANCEIRO E DE INTEGRAÇÃO REGIONAL - DAFIR', styles2['default'])],
               ]
        t3=Table(data, 2.35*inch)
        t3.setStyle(TableStyle([#('GRID',(0,0),(-1,1),1,(0,0,0)),
                                ('BOX',(0,0),(-1,-1),1,(0,0,0)),
                                ('LINEABOVE',(0,0),(2,1),1,(0,0,0)),
                                ('LINEBEFORE',(0,0),(-1,-1),1,(0,0,0)),
                                ('VALIGN',(0,-1),(-1,-1),'TOP'),
                                #('ALIGN',(0,0),(0,0),'LEFT'),
                              ]))



        '''
        t=Table(data)
        t._argW[3]=1.5*inch
        '''
        texto = 'A Agência Estadual de Vigilância Sanitária através da Diretoria Técnica de Medicamentos, Alimentos, Produtos e Toxicologia concede ao estabelecimento EMPRESA EXEMPLO LTDA a presente Autorização de Funcionamento de nº 6224 de acordo com as disposições da Lei nº 7069 de 12 de abril de 2002, Art. 4º, VI.'
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        I = Image(os.path.join(BASE_DIR, 'segCadastro/static/img/cabecalhoAlvara.jpg'))
        elements.append(I)
        elements.append(Paragraph('Autorização de Funcionamento', styles2['title']))
        elements.append(t)
        elements.append(Paragraph('Processo nº: I-122016.2016.0', styles2['default']))
        elements.append(Paragraph( texto, styles2['default']))
        elements.append(Paragraph('Número: 6224', styles2['default']))
        elements.append(Paragraph('Razão Social: EMPRESA EXEMPLO LTDA', styles2['default']))
        elements.append(Paragraph('Nome Fantasia: EMPRESA EXEMPLO, CNPJ: 08.201.325/0001-25', styles2['default']))
        elements.append(Paragraph('Município: COXIXOLA, CEP: 58.074-000', styles2['default']))
        elements.append(Paragraph('Endereço: RUA JOSÉ DOS ANZÓIS, S/N - CENTRO', styles2['default']))
        elements.append(Paragraph('Resposável Legal: AUGUSTO JOSÉ HENRIQUES', styles2['default']))
        elements.append(Paragraph('', styles2['default']))
        elements.append(t2)
        elements.append(Paragraph('', styles2['default']))
        elements.append(t3)
        elements.append(Paragraph('Todas as ações realizadas acima são por meio de Autenticação Eletrônica de Usuários', styles2['default']))
        elements.append(Paragraph('', styles2['default']))
        elements.append(Paragraph('Código de Autenticidade: bec8bb93-ab93-4956-9862-a_l1uyhQM', styles2['default']))

        #for i, user in enumerate(users):
            #elements.append(Paragraph(user.get_full_name(), styles['Normal']))

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
