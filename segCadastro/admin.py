# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import Responsavel, CBO, Tipo_Servico_Saude
from .models import Tipo_Equipamento_Saude, Autorizacao_Funcionamento
from .models import Pessoa_Fisica, Pessoa_Juridica, Equipamento_Saude
from .models import Atividade, Redesim, Natureza_Juridica
from .models import Estabelecimento_Desempenha_Atv
from .models import Assunto_Processo, Processo, Documento, Setor
from .models import Processo_Tramita_Setor, Valor_UFR, Atividade, Categoria_Atividade

class EquipamentoInline(admin.TabularInline):
    model = Equipamento_Saude
    extra = 1

class AutorizacaoInline(admin.TabularInline):
    model = Autorizacao_Funcionamento
    extra = 1

class DocumentoInline(admin.TabularInline):
    model = Documento
    extra = 3

class Estabelecimento_Desempenha_AtvAdmin(admin.ModelAdmin):
    filter_horizontal = ('ResponsavelTecnico',)

class ProcessoAdmin(admin.ModelAdmin):
    inlines = [DocumentoInline]

class Pessoa_FisicaAdmin(admin.ModelAdmin):
    search_fields = ['Nome', 'CPF', 'Municipio']
    list_display = ('Nome', 'CPF', 'Municipio')
    filter_horizontal = ('TiposServicoSaude', 'Atividade')
    fieldsets = [
        (None,               {'fields': [
                                        'TipoCadastro', 'Pasta', 'CNES',
                                        'Nome', 'CPF', 'SiglaConselhoClasse',
                                        'InscricaoConselhoClasse', 'CEP',
                                        'Endereco', 'Numero', 'Complemento',
                                        'PontoReferencia', 'Bairro', 'Municipio',
                                        'TelefonePrimario', 'TelefoneSecundario',
                                        'Email', 'Obs',
                                        ]}),
        ('Caracterização do Serviço de Saúde', {'fields': ['TiposServicoSaude']}),
        ('Estabelecimento de Saúde de Natureza Ambulatorial - Informações Estruturais',
            {'fields': [
                       'ConsultorioOdontologico', 'Equipo',
                       'ConsultorioMedicoPediatrico', 'ConsultorioMedicoFeminino',
                       'ConsultorioMedicoMasculino', 'ConsultorioMedicoOutro',
                       'OutroConsultorio', 'SalaPediatrico',
                       'LeitoRepousoPediatrico', 'SalaFeminino',
                       'LeitoRepousoFeminino', 'SalaMasculino',
                       'LeitoRepousoMasculino', 'SalaOutro', 'LeitoRepousoOutro',
                       'SalaPequenaCirurgia', 'SalaNebulizacao', 'SalaGesso',
                       'SalaImunizacao', 'SalaCurativo', 'SalaEnfermagem',
                       'SalaCirurgiaAmbulatorial', 'SalaQuimioterapia',
                       'PoltronaQuimioterapia', 'SalaDialise', 'PoltronaDialise',
                       ]}),
        ('Leitos de Estabelecimentos de Saúde com Internação e de Unidades de Urgência / Emergência',
            {'fields': [
                       'LtIntCirurgicaBucoMaxiloFacial', 'LtIntCirurgicaCardiologia',
                       'LtIntCirurgicaCirurgiaGeral', 'LtIntCirurgicaEndocrinologia',
                       'LtIntCirurgicaGenterologia', 'LtIntCirurgicaGinecologia',
                       'LtIntCirurgicaLeitoDia', 'LtIntCirurgicaNefroUrologia',
                       'LtIntCirurgicaNeurocirurgia', 'LtIntCirurgicaObstetricia',
                       'LtIntCirurgicaOftalmologia', 'LtIntCirurgicaOncologia',
                       'LtIntCirurgicaOrtTraumatologia', 'LtIntCirurgicaOtorrinolaringo',
                       'LtIntCirurgicaPlastica', 'LtIntCirurgicaToracica',
                       'LtIntClinicaAIDS', 'LtIntClinicaCardiologia',
                       'LtIntClinicaCronicos', 'LtIntClinicaDermatologia',
                       'LtIntClinicaGeriatria', 'LtIntClinicaHansenologia',
                       'LtIntClinicaHematologia', 'LtIntClinicaLeitoDia',
                       'LtIntClinicaNefroUrologia', 'LtIntClinicaNeonatologia',
                       'LtIntClinicaNeurologia', 'LtIntClinicaObstetricia',
                       'LtIntClinicaOncologia', 'LtIntClinicaPediatria',
                       'LtIntClinicaPneumologia', 'LtIntClinicaPsiquiatria',
                       'LtIntClinicaReabilitacao', 'LtIntClinicaTisiologia',
                       'UrgIntUTIAdulto', 'UrgIntUTIInfantil',
                       'UrgIntUTINeonatal', 'UrgIntUTIUnidadeIntermediaria',
                       'UrgIntUTIUnidadeInterNeonatal', 'UrgIntUTIUnidadeIsolamento',
                       'UrgLtObservacaoProntoSocorro',
                       ]}),
    ]
    inlines = [EquipamentoInline]

class Pessoa_JuridicaAdmin(admin.ModelAdmin):
    search_fields = ['RazaoSocial', 'CNPJ', 'Municipio']
    list_display = ('RazaoSocial', 'CNPJ', 'Municipio')
    filter_horizontal = ('ResponsaveisLegais', 'TiposServicoSaude', 'ProfissionaisCCIH')
    fieldsets = [
        (None,               {'fields': [
                                        'TipoCadastro', 'Pasta', 'CNES',
                                        'EstabelecimentoMantenedor',
                                        'RazaoSocial', 'NomeFantasia', 'CNPJ',
                                        'NIRE', 'NaturezaJuridica', 'Porte',
                                        'Tipo', 'CNPJMatriz', 'Natureza',
                                        'InicioAtividades', 'TerminoAtividades',
                                        'Situacao', 'ObjetoSocial',
                                        'AreaUtilizada', 'Metragem',
                                        'CEP', 'Endereco', 'Numero',
                                        'Complemento', 'PontoReferencia',
                                        'Bairro', 'Municipio',
                                        'TelefonePrimario', 'TelefoneSecundario',
                                        'Email', 'Obs',
                                        ]}),
        ('Responsável(eis) Legal(ais)', {'fields': ['ResponsaveisLegais']}),
        ('Caracterização do Serviço de Saúde', {'fields': ['TiposServicoSaude']}),
        ('Estabelecimento de Saúde de Natureza Ambulatorial - Informações Estruturais',
            {'fields': [
                       'ConsultorioOdontologico', 'Equipo',
                       'ConsultorioMedicoPediatrico', 'ConsultorioMedicoFeminino',
                       'ConsultorioMedicoMasculino', 'ConsultorioMedicoOutro',
                       'OutroConsultorio', 'SalaPediatrico',
                       'LeitoRepousoPediatrico', 'SalaFeminino',
                       'LeitoRepousoFeminino', 'SalaMasculino',
                       'LeitoRepousoMasculino', 'SalaOutro', 'LeitoRepousoOutro',
                       'SalaPequenaCirurgia', 'SalaNebulizacao', 'SalaGesso',
                       'SalaImunizacao', 'SalaCurativo', 'SalaEnfermagem',
                       'SalaCirurgiaAmbulatorial', 'SalaQuimioterapia',
                       'PoltronaQuimioterapia', 'SalaDialise', 'PoltronaDialise',
                       ]}),
        ('Comissão de Controle de Infecção Hospitalar / CCIH', {'fields': ['ProfissionaisCCIH']}),
        ('Leitos de Estabelecimentos de Saúde com Internação e de Unidades de Urgência / Emergência',
            {'fields': [
                       'LtIntCirurgicaBucoMaxiloFacial', 'LtIntCirurgicaCardiologia',
                       'LtIntCirurgicaCirurgiaGeral', 'LtIntCirurgicaEndocrinologia',
                       'LtIntCirurgicaGenterologia', 'LtIntCirurgicaGinecologia',
                       'LtIntCirurgicaLeitoDia', 'LtIntCirurgicaNefroUrologia',
                       'LtIntCirurgicaNeurocirurgia', 'LtIntCirurgicaObstetricia',
                       'LtIntCirurgicaOftalmologia', 'LtIntCirurgicaOncologia',
                       'LtIntCirurgicaOrtTraumatologia', 'LtIntCirurgicaOtorrinolaringo',
                       'LtIntCirurgicaPlastica', 'LtIntCirurgicaToracica',
                       'LtIntClinicaAIDS', 'LtIntClinicaCardiologia',
                       'LtIntClinicaCronicos', 'LtIntClinicaDermatologia',
                       'LtIntClinicaGeriatria', 'LtIntClinicaHansenologia',
                       'LtIntClinicaHematologia', 'LtIntClinicaLeitoDia',
                       'LtIntClinicaNefroUrologia', 'LtIntClinicaNeonatologia',
                       'LtIntClinicaNeurologia', 'LtIntClinicaObstetricia',
                       'LtIntClinicaOncologia', 'LtIntClinicaPediatria',
                       'LtIntClinicaPneumologia', 'LtIntClinicaPsiquiatria',
                       'LtIntClinicaReabilitacao', 'LtIntClinicaTisiologia',
                       'UrgIntUTIAdulto', 'UrgIntUTIInfantil',
                       'UrgIntUTINeonatal', 'UrgIntUTIUnidadeIntermediaria',
                       'UrgIntUTIUnidadeInterNeonatal', 'UrgIntUTIUnidadeIsolamento',
                       'UrgLtObservacaoProntoSocorro',
                       ]}),
    ]
    inlines = [EquipamentoInline, AutorizacaoInline]

admin.site.register(Responsavel)
admin.site.register(CBO)
admin.site.register(Tipo_Servico_Saude)
admin.site.register(Tipo_Equipamento_Saude)
admin.site.register(Pessoa_Fisica, Pessoa_FisicaAdmin)
admin.site.register(Pessoa_Juridica, Pessoa_JuridicaAdmin)
admin.site.register(Estabelecimento_Desempenha_Atv, Estabelecimento_Desempenha_AtvAdmin)
admin.site.register(Redesim)
admin.site.register(Processo, ProcessoAdmin)
admin.site.register(Assunto_Processo)
admin.site.register(Setor)
admin.site.register(Processo_Tramita_Setor)
admin.site.register(Valor_UFR)
admin.site.register(Atividade)
admin.site.register(Categoria_Atividade)
admin.site.register(Natureza_Juridica)
