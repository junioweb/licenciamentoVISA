# -*- encoding: utf-8 -*-
import uuid
from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Municipio(models.Model):
    IBGE = models.PositiveIntegerField('Código IBGE', primary_key=True, validators=[MaxValueValidator(999999)])
    Nome = models.CharField('Nome do Município', max_length=45)

    def __unicode__(self):
        return unicode(self.IBGE)+' - '+self.Nome

    class Meta:
        ordering = ['Nome']
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'

class Tipo_Servico_Saude(models.Model):
    Tipo = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
	return self.Tipo

    class Meta:
        verbose_name = 'Tipo de Serviço de Saúde'
        verbose_name_plural = 'Tipos de Serviços de Saúde'

class Tipo_Equipamento_Saude(models.Model):
    GERAL = 0
    EMED = 1
    EARTQR = 2
    COMFS = 3
    FONTS = 4
    PUSOVET = 5

    CATEGORIA_CHOICES = (
        (GERAL, 'Geral'),
        (EMED, 'Para Medições'),
        (EARTQR, 'Auxiliares para Radiometria e Testes de Qualidade em Radiodiagnóstico'),
        (COMFS, 'Com Fontes Seladas'),
        (FONTS, 'Fonstes Seladas'),
        (PUSOVET, 'Para Uso Veterinário'),
    )
    Categoria = models.IntegerField(choices=CATEGORIA_CHOICES)
    Tipo = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.get_Categoria_display()+' - '+self.Tipo

    class Meta:
        verbose_name = 'Tipo de Equipamento de Saúde'
        verbose_name_plural = 'Tipos de Equipamentos de Saúde'

class CBO(models.Model):
    Codigo = models.CharField('Código', max_length=6)
    Ocupacao = models.CharField('Ocupação', max_length=100)

    def __unicode__(self):
        return self.Codigo+' - '+self.Ocupacao

    class Meta:
        verbose_name = 'CBO'
        verbose_name_plural = 'CBO\'s'

class Responsavel(models.Model):
    Nome = models.CharField(max_length=100)
    CPF = models.CharField(max_length=11, unique=True)
    SiglaConselhoClasse = models.CharField('Sigla do Conselho de Classe', max_length=10, blank=True)
    InscricaoConselhoClasse = models.CharField('Inscrição no Conselho de Classe', max_length=25, blank=True)
    CEP = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)])
    Endereco = models.CharField('Endereço', max_length=100)
    Numero = models.CharField('Número', max_length=10)
    Complemento = models.CharField(max_length=50, blank=True)
    Bairro = models.CharField(max_length=50)
    TelefonePrimario = models.BigIntegerField('Telefone Primário', validators=[MaxValueValidator(99999999999)])
    TelefoneSecundario = models.BigIntegerField('Telefone Secundário', validators=[MaxValueValidator(99999999999)], null=True, blank=True)
    Email = models.EmailField(max_length=150)
    Municipio = models.ForeignKey(
        Municipio,
        verbose_name='Municípios',
        null=True,
        blank=True,
    )
    CBO = models.ForeignKey(
        CBO,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.CPF+' - '+self.Nome

    class Meta:
        verbose_name = 'Responsável'
        verbose_name_plural = 'Responsáveis'

class Categoria_Atividade(models.Model):
    Grupo = models.CharField(max_length=100)
    Subgrupo = models.CharField(max_length=100, blank=True)
    Agrupamento = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
	return self.Agrupamento

    class Meta:
	unique_together = (('Grupo', 'Agrupamento'),)

class Atividade(models.Model):
    Categoria = models.ForeignKey(Categoria_Atividade, null=True)
    Secao = models.CharField('Seção', max_length=1)
    Divisao = models.CharField('Divisão', max_length=2)
    Grupo = models.CharField(max_length=3)
    Classe = models.CharField(max_length=5)
    Subclasse = models.CharField(max_length=7, unique=True)
    Denominacao = models.CharField('Denominação', max_length=150)
    Risco = models.CharField(max_length=1)
    BaseLegal = models.TextField('Base Legal', blank=True)
    Nota = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.Subclasse)+' - '+self.Denominacao

class Estabelecimento(models.Model):
    PRECAD = 0
    CADDEF = 1

    TIPO_CADASTRO_CHOICES = (
        (PRECAD, 'Pré-cadastro'),
        (CADDEF, 'Cadastro Definitivo'),
    )
    TipoCadastro = models.IntegerField('Tipo de Cadastro', choices=TIPO_CADASTRO_CHOICES)
    Pasta = models.IntegerField(null=True, blank=True, unique=True)
    CEP = models.CharField(max_length=8, blank=True)
    Endereco = models.CharField('Endereço', max_length=100)
    Numero = models.CharField('Número', max_length=10)
    Complemento = models.CharField(max_length=50, blank=True)
    PontoReferencia = models.CharField('Ponto de Referência', max_length=50, blank=True)
    Bairro = models.CharField(max_length=50)
    TelefonePrimario = models.BigIntegerField('Telefone Primário', validators=[MaxValueValidator(99999999999)])
    TelefoneSecundario = models.BigIntegerField('Telefone Secundário', validators=[MaxValueValidator(99999999999)], null=True, blank=True)
    Email = models.EmailField(max_length=150)
    CNES = models.IntegerField(blank=True, null=True)
    Obs = models.TextField('Observação', blank=True)
    ConsultorioMedicoPediatrico = models.IntegerField('Consultório Médico Pediátrico', blank=True, null=True)
    ConsultorioMedicoFeminino = models.IntegerField('Consultório Médico Feminino', blank=True, null=True)
    ConsultorioMedicoMasculino = models.IntegerField('Consultório Médico Masculino', blank=True, null=True)
    ConsultorioMedicoOutro = models.IntegerField('Outro Consultório Médico', blank=True, null=True)
    OutroConsultorio = models.IntegerField('Outro Consultório', blank=True, null=True)
    SalaPediatrico = models.IntegerField('Sala Pediátrico', blank=True, null=True)
    LeitoRepousoPediatrico = models.IntegerField('Leito de Repouso (Observação) Pediátrico', blank=True, null=True)
    SalaFeminino = models.IntegerField('Sala Feminino', blank=True, null=True)
    LeitoRepousoFeminino = models.IntegerField('Leito de Repouso (Observação) Feminino', blank=True, null=True)
    SalaMasculino = models.IntegerField('Sala Masculino', blank=True, null=True)
    LeitoRepousoMasculino = models.IntegerField('Leito de Repouso (Observação) Masculino', blank=True, null=True)
    SalaOutro = models.IntegerField('Outra Sala', blank=True, null=True)
    LeitoRepousoOutro = models.IntegerField('Outro Leito de Repouso (Observação)', blank=True, null=True)
    ConsultorioOdontologico = models.IntegerField('Consultório Odontológico', blank=True, null=True)
    Equipo = models.IntegerField(blank=True, null=True)
    SalaPequenaCirurgia = models.IntegerField('Sala Pequena Cirurgia', blank=True, null=True)
    SalaNebulizacao = models.IntegerField('Sala Nebulização', blank=True, null=True)
    SalaGesso = models.IntegerField('Sala Gesso', blank=True, null=True)
    SalaImunizacao = models.IntegerField('Sala Imunização', blank=True, null=True)
    SalaCurativo = models.IntegerField('Sala Curativo', blank=True, null=True)
    SalaEnfermagem = models.IntegerField('Sala Enfermagem', blank=True, null=True)
    SalaCirurgiaAmbulatorial = models.IntegerField('Sala Cirurgia Ambulatorial', blank=True, null=True)
    SalaQuimioterapia = models.IntegerField('Sala Quimioterapia', blank=True, null=True)
    PoltronaQuimioterapia = models.IntegerField('Poltrona Quimioterapia', blank=True, null=True)
    SalaDialise = models.IntegerField('Sala Diálise', blank=True, null=True)
    PoltronaDialise = models.IntegerField('Poltrona Diálise', blank=True, null=True)
    LtIntCirurgicaBucoMaxiloFacial = models.IntegerField('Cirúrgica Buco Maxilo Facial', blank=True, null=True)
    LtIntCirurgicaCardiologia = models.IntegerField('Cirúrgica Cardiologia', blank=True, null=True)
    LtIntCirurgicaCirurgiaGeral = models.IntegerField('Cirúrgica Cirurgia Geral', blank=True, null=True)
    LtIntCirurgicaEndocrinologia = models.IntegerField('Cirúrgica Endocrinologia', blank=True, null=True)
    LtIntCirurgicaGenterologia = models.IntegerField('Cirúrgica Gastroenterologia', blank=True, null=True)
    LtIntCirurgicaGinecologia = models.IntegerField('Cirúrgica Ginecologia', blank=True, null=True)
    LtIntCirurgicaLeitoDia = models.IntegerField('Cirúrgica Leito / Dia', blank=True, null=True)
    LtIntCirurgicaNefroUrologia = models.IntegerField('Cirúrgica Nefrologia / Urologia', blank=True, null=True)
    LtIntCirurgicaNeurocirurgia = models.IntegerField('Cirúrgica Neurocirurgia', blank=True, null=True)
    LtIntCirurgicaObstetricia = models.IntegerField('Cirúrgica Obstetrícia', blank=True, null=True)
    LtIntCirurgicaOftalmologia = models.IntegerField('Cirúrgica Oftalmologia', blank=True, null=True)
    LtIntCirurgicaOncologia = models.IntegerField('Cirúrgica Oncologia', blank=True, null=True)
    LtIntCirurgicaOrtTraumatologia = models.IntegerField('Cirúrgica Ortopedia / Traumatologia', blank=True, null=True)
    LtIntCirurgicaOtorrinolaringo = models.IntegerField('Cirúrgica Otorrinolaringologia', blank=True, null=True)
    LtIntCirurgicaPlastica = models.IntegerField('Cirúrgica Plástica', blank=True, null=True)
    LtIntCirurgicaToracica = models.IntegerField('Cirúrgica Torácica', blank=True, null=True)
    LtIntClinicaAIDS = models.IntegerField('Clínica AIDS', blank=True, null=True)
    LtIntClinicaCardiologia = models.IntegerField('Clínica Cardiologia', blank=True, null=True)
    LtIntClinicaClinicaGeral = models.IntegerField('Clínica - Clínica Geral', blank=True, null=True)
    LtIntClinicaCronicos = models.IntegerField('Clínica Crônicos', blank=True, null=True)
    LtIntClinicaDermatologia = models.IntegerField('Clínica Dermatologia', blank=True, null=True)
    LtIntClinicaGeriatria = models.IntegerField('Clínica Geriatria', blank=True, null=True)
    LtIntClinicaHansenologia = models.IntegerField('Clínica Hansenologia', blank=True, null=True)
    LtIntClinicaHematologia = models.IntegerField('Clínica Hematologia', blank=True, null=True)
    LtIntClinicaLeitoDia = models.IntegerField('Clínica Leito / Dia', blank=True, null=True)
    LtIntClinicaNefroUrologia = models.IntegerField('Clínica Nefro / Urologia', blank=True, null=True)
    LtIntClinicaNeonatologia = models.IntegerField('Clínica Neonatologia', blank=True, null=True)
    LtIntClinicaNeurologia = models.IntegerField('Clínica Neurologia', blank=True, null=True)
    LtIntClinicaObstetricia = models.IntegerField('Clínica Obstetrícia', blank=True, null=True)
    LtIntClinicaOncologia = models.IntegerField('Clínica Oncologia', blank=True, null=True)
    LtIntClinicaPediatria = models.IntegerField('Clínica Pediatria', blank=True, null=True)
    LtIntClinicaPneumologia = models.IntegerField('Clínica Pneumologia', blank=True, null=True)
    LtIntClinicaPsiquiatria = models.IntegerField('Clínica Psiquiatria', blank=True, null=True)
    LtIntClinicaReabilitacao = models.IntegerField('Clínica Reabilitação', blank=True, null=True)
    LtIntClinicaTisiologia = models.IntegerField('Clínica Tisiologia', blank=True, null=True)
    UrgIntUTIAdulto = models.IntegerField('UTI Adulto', blank=True, null=True)
    UrgIntUTIInfantil = models.IntegerField('UTI Infantil', blank=True, null=True)
    UrgIntUTINeonatal = models.IntegerField('UTI Neonatal', blank=True, null=True)
    UrgIntUTIUnidadeIntermediaria = models.IntegerField('Unidade Intermediária', blank=True, null=True)
    UrgIntUTIUnidadeInterNeonatal = models.IntegerField('Unidade Intermediária Neonatal', blank=True, null=True)
    UrgIntUTIUnidadeIsolamento = models.IntegerField('Unidade de Isolamento', blank=True, null=True)
    UrgLtObservacaoProntoSocorro = models.IntegerField('Unidade de Urgência / Emergência (Pronto-Socorro) - Leitos Observação', blank=True, null=True)

    Atividade = models.ManyToManyField(Atividade, through='Estabelecimento_Desempenha_Atv')
    Municipio = models.ForeignKey(
        Municipio,
        verbose_name='Município',
        null=True,
        blank=True
        )
    TiposServicoSaude = models.ManyToManyField(
        Tipo_Servico_Saude,
        blank=True,
        verbose_name='Tipos do Serviço de Saúde',
    )

    child_class_names = (
    'Pessoa_Fisica',
    'Pessoa_Juridica',
    )
    def child_object(self):
        for child_class_name in self.child_class_names:
          try:
            return self.__getattribute__(child_class_name.lower())
          except eval(child_class_name).DoesNotExist:
            pass
        return self

    def __unicode__(self):
        pessoa = self.child_object()

        if hasattr(pessoa, 'Nome'):
            return pessoa.CPF+' - '+pessoa.Nome
        elif hasattr(pessoa, 'RazaoSocial'):
            return pessoa.CNPJ+' - '+pessoa.RazaoSocial

class Pessoa_Fisica(Estabelecimento):
    Nome = models.CharField(max_length=100)
    CPF = models.CharField(max_length=11)
    SiglaConselhoClasse = models.CharField('Sigla do Conselho de Classe', max_length=10, blank=True)
    InscricaoConselhoClasse = models.CharField('Inscrição no Conselho de Classe', max_length=25, blank=True)

    def __unicode__(self):
        return self.CPF+' - '+self.Nome

    class Meta:
        verbose_name = 'Estabelecimento - Pessoa Física'
        verbose_name_plural = 'Estabelecimentos - Pessoa Física'

class Natureza_Juridica(models.Model):
    Codigo = models.PositiveIntegerField(unique=True)
    Nome = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.Codigo)+' - '+self.Nome

class Pessoa_Juridica(Estabelecimento):
    AGRICULTURA_FAMILIAR = 1
    ECONOMIA_SOLIDARIA = 2
    MEI = 3
    ME = 4
    PEQUENO = 5
    GRANDE = 6
    MATRIZ = 1
    FILIAL = 2
    PRIVADA = 1
    PUBLICA = 2
    FILANTROPICA = 3
    ATIVA = 0
    SSTATUS = 1
    CAN94 = 2
    EXTIN = 3
    CONVE = 4
    CINDIDAT = 5
    TRASF = 6
    FALIDA = 7
    CANCEL = 8
    ATVPRO = 9
    CANMEI = 10
    SUSPTA = 11

    PORTE_CHOICES = (
        (AGRICULTURA_FAMILIAR, 'Agricultura Familiar'),
        (ECONOMIA_SOLIDARIA, 'Economia Solidária'),
        (MEI, 'Microempreendedor Individual'),
        (ME, 'Micro Empresa'),
        (PEQUENO, 'Pequeno Porte'),
        (GRANDE, 'Grande Porte'),
    )
    TIPO_CHOICES = (
        (MATRIZ, 'Matriz'),
        (FILIAL, 'Filial'),
    )
    NATUREZA_CHOICES = (
        (PRIVADA, 'Privada'),
        (PUBLICA, 'Pública'),
        (FILANTROPICA, 'Filantrópica'),
    )
    SITUACAO_CHOICES = (
        (ATIVA, 'ATIVA'),
        (SSTATUS, 'SEM STATUS'),
        (CAN94, 'CANCELADA - ART.60 LEI 8934/94'),
        (EXTIN, 'EXTINTA'),
        (CONVE, 'CONVERTIDA SOC. CIVIL/SIMPLES'),
        (CINDIDAT, 'CINDIDA TOTALMENTE'),
        (TRASF, 'TRANSFERIDA PARA OUTRA UF'),
        (FALIDA, 'FALIDA'),
        (CANCEL, 'CANCELADA'),
        (ATVPRO, 'REGISTRO ATIVO PROVISÓRIO'),
        (CANMEI, 'CANCELADA-MEI'),
        (SUSPTA, 'SUSPENSÃO TEMPORÁRIA DE ATIVIDADES'),
    )
    RazaoSocial = models.CharField('Razão Social', max_length=150)
    NomeFantasia = models.CharField('Nome Fantasia', max_length=150, blank=True)
    CNPJ = models.CharField(max_length=14, blank=True, unique=True)
    NIRE = models.CharField(max_length=12, blank=True)
    NaturezaJuridica = models.ForeignKey(Natureza_Juridica, verbose_name='Natureza Jurídica', null=True, blank=True)
    Porte = models.IntegerField(choices=PORTE_CHOICES, null=True, blank=True)
    Tipo = models.IntegerField(choices=TIPO_CHOICES)
    CNPJMatriz = models.CharField('CNPJ Matriz', max_length=14, blank=True)
    Natureza = models.IntegerField(choices=NATUREZA_CHOICES)
    InicioAtividades = models.DateField('Início das Atividades', blank=True, null=True)
    TerminoAtividades = models.DateField('Término das Atividades', blank=True, null=True)
    Situacao = models.IntegerField('Situação', choices=SITUACAO_CHOICES, default=0)
    ObjetoSocial = models.TextField('Objeto Social', blank=True)
    AreaUtilizada = models.CharField('Área Utilizada', max_length=13, blank=True)
    Metragem = models.CharField(max_length=13, blank=True)

    ResponsaveisLegais = models.ManyToManyField(
        Responsavel,
        related_name='%(app_label)s_%(class)s_responsavel_legal',
        verbose_name='Responsáveis Legais',
        blank=True,
    )
    ProfissionaisCCIH = models.ManyToManyField(
        Responsavel,
        related_name='%(app_label)s_%(class)s_profissional_ccih',
        blank=True,
        verbose_name='Comissão de Controle de Infecção Hospitalar / CCIH',
    )
    EstabelecimentoMantenedor = models.ForeignKey(
        'Pessoa_Juridica',
        related_name='%(app_label)s_%(class)s_estabelecimeto_mantenedor',
        blank=True,
        null=True,
        verbose_name='Estabelecimento Mantenedor',
    )

    def __unicode__(self):
        return self.CNPJ+' - '+self.RazaoSocial+' ('+self.NomeFantasia+')'

    class Meta:
        verbose_name = 'Estabelecimento - Pessoa Jurídica'
        verbose_name_plural = 'Estabelecimentos - Pessoa Jurídica'

class Equipamento_Saude(models.Model):
    TipoEquip = models.ForeignKey(Tipo_Equipamento_Saude, null=True, blank=True)
    Caracteristicas = models.TextField('Características', null=True, blank=True)
    Estabelecimento = models.ForeignKey(Estabelecimento)

    class Meta:
        verbose_name = 'Equipamento de Saúde'
        verbose_name_plural = 'Equipamentos de Saúde'

class Autorizacao_Funcionamento(models.Model):
    MEDICAMENTO = 'MD'
    DROGARIA = 'DR'
    SANEANTE = 'SN'
    CORRELATO = 'CR'
    COSMETICO = 'CO'
    AFE = 'AFE'
    AE = 'AE'
    CATEGORIA_AF_CHOICES = (
        (DROGARIA, 'Farmácia / Drogaria'),
        (CORRELATO, 'Produto para Saúde / Correlato'),
        (SANEANTE, 'Saneante Domissanitário'),
        (COSMETICO, 'Cosmetico / Perfume / Produto de Higiene'),
        (MEDICAMENTO, 'Medicamento / Insumo Farmacêutico'),
    )
    TIPO_AF_CHOICES = (
        (AFE, 'AFE - Autorização de Funcionamento da Empresa'),
        (AE, 'AE - Autorização Especial')
    )
    NumeroAF = models.PositiveIntegerField('Número da Autorização', primary_key=True, validators=[MaxValueValidator(9999999)])
    DataPublicacao = models.DateField('Data da Publicação')
    TipoAF = models.CharField(max_length=3,
                            choices=TIPO_AF_CHOICES)
    Categoria = models.CharField(max_length=2,
                                 choices=CATEGORIA_AF_CHOICES)
    PessoaJuridica = models.ForeignKey(Pessoa_Juridica)

    class Meta:
        verbose_name = 'Autorização de Funcionamento'
        verbose_name_plural = 'Autorizações de Funcionamento'

class Veiculo(models.Model):
    Renavam = models.BigIntegerField(validators=[MaxValueValidator(999999999999999)])
    Nome = models.CharField(max_length=150)
    CNPJ = models.CharField(max_length=14, blank=True)
    CPF = models.CharField(max_length=11, blank=True)
    Placa = models.CharField(max_length=7)
    UF = models.CharField(max_length=2)
    Chassi = models.CharField(max_length=17)
    TipoVeiculo = models.CharField(max_length=8)
    MarcaModelo = models.CharField('Marca / Modelo', max_length=50)
    AnoFab = models.CharField('Ano de Fabricação', max_length=4)
    AnoMod = models.CharField('Ano de Modelo', max_length=4)
    CNES = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    Obs = models.TextField('Observação', blank=True)

    def __unicode__(self):
        return 'Placa: '+self.Placa+' - Tipo: '+self.TipoVeiculo+' - '+self.Nome

    class Meta:
        ordering = ['Placa']
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

class Estabelecimento_Desempenha_Atv(models.Model):
    Estabelecimento = models.ForeignKey(Estabelecimento, verbose_name='Estabelecimento')
    Atividade = models.ForeignKey(Atividade, verbose_name='Atividade(s) Econômica(s)')
    Manipular = models.BooleanField()
    Fracionar = models.BooleanField()
    Dispensar = models.BooleanField()
    AferirParam = models.BooleanField('Aferir parâmetros fisiológicos e bioquímico')
    PrestarAten = models.BooleanField('Prestar atenção farmacêutica domiciliar')
    AdmAplicar = models.BooleanField('Administrar/aplicar medicamentos')
    Perfurar = models.BooleanField('Perfurar lóbulo auricular para colocação de brinco')
    DispRemoto = models.BooleanField('Dispensar por meio remoto')
    Fabricar = models.BooleanField()
    Transformar = models.BooleanField()
    Purificar = models.BooleanField()
    Extrair = models.BooleanField()
    Fragmentar = models.BooleanField()
    Sintetizar = models.BooleanField()
    EstRadiacaoIon = models.BooleanField('Esterelizar radiação ionizante')
    EstETO = models.BooleanField('Esterelizar ETO')
    EstOutras = models.BooleanField('Esterelizar outras')
    Reprocessar = models.BooleanField()
    Irradiar = models.BooleanField()
    Transportar = models.BooleanField()
    Expedir = models.BooleanField()
    Armazenar = models.BooleanField()
    Embalar = models.BooleanField()
    Distribuir = models.BooleanField()
    Importar = models.BooleanField()
    ImpUsoProprio = models.BooleanField('Importar para uso próprio')
    Exportar = models.BooleanField()
    RealEtapFab = models.BooleanField('Realizar etapas de fabricação')

    ResponsavelTecnico = models.ManyToManyField(
                                                Responsavel,
                                                blank=True,
                                                verbose_name='Responsável(eis) Técnico(s)',
                                                )
    Veiculo = models.ForeignKey(Veiculo, null=True, blank=True)
    Setor = models.ForeignKey('Setor')

    def __unicode__(self):
        if self.Veiculo != None:
            return unicode(self.Estabelecimento)+'<=('+unicode(self.Veiculo)+')=>'+unicode(self.Atividade)
        else:
            return unicode(self.Estabelecimento)+' => '+unicode(self.Atividade)

    class Meta:
        verbose_name = 'Caracterização da Atividade Econômica'
        verbose_name_plural = 'Caracterizações das Atividades Econômicas'

class Assunto_Processo(models.Model):
    Nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.Nome

    class Meta:
        verbose_name = 'Assunto do Processo'
        verbose_name_plural = 'Assuntos do Processo'

class Processo(models.Model):
    INICIAL = 'I'
    RENOVACAO = 'R'
    ALTERACAO = 'A'
    OUTRO = 'O'
    TIPO_CHOICES = (
        (INICIAL, 'Inicial'),
        (RENOVACAO, 'Renovação'),
        (ALTERACAO, 'Alteração'),
        (OUTRO, 'Outro'),
    )

    Tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    Numero = models.AutoField(primary_key=True)
    Ano = models.CharField(max_length=4)
    DataEmissao = models.DateTimeField(auto_now_add=True)
    ProcessoMae = models.ForeignKey('self', null=True, blank=True, verbose_name='Processo Mãe')
    Estabelecimento = models.ForeignKey(Estabelecimento, null=True, blank=True)
    Exercicio = models.CharField(max_length=4)
    Assunto = models.ForeignKey(Assunto_Processo)
    Obs = models.TextField(blank=True)
    Atividade_Estabelecimento = models.ManyToManyField(
                                            Estabelecimento_Desempenha_Atv,
                                            related_name="atividades_estab",
                                            blank=True,
                                            verbose_name="Atividade ou Atividade/Veículo"
                                        )
    TramitaSetor = models.ManyToManyField('Setor', through='Processo_Tramita_Setor', blank=True)

    def __unicode__(self):
        if self.ProcessoMae == None:
            processoMae = 0
        else:
            processoMae = 1

        return self.Tipo+'-'+unicode(self.Numero)+self.Ano+'.'+self.Exercicio+'.'+unicode(processoMae)+' ('+unicode(self.Estabelecimento)+')'

    class Meta:
        unique_together = (('Tipo', 'Numero', 'Ano'),)

class Situacao(models.Model):
    Situacao = models.CharField(max_length=50)
    Obs = models.TextField(blank=True)
    Processo = models.ForeignKey(Processo)

    def __unicode__(self):
        return self.Processo+' - '+self.Situacao

    class Meta:
        verbose_name = 'Situação de Processo'
        verbose_name_plural = 'Situações de Processos'

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.Processo, filename)

class Documento(models.Model):
    ASSUNTO_CHOICES = (
        ('AUTORIZAÇÃO DE FUNCIONAMENTO (AGEVISA)', 'AUTORIZAÇÃO DE FUNCIONAMENTO (AGEVISA)'),
        ('RELATÓRIO TÉCNICO DE INSPEÇÃO', 'RELATÓRIO TÉCNICO DE INSPEÇÃO'),
        ('TERMO DE INSPEÇÃO', 'TERMO DE INSPEÇÃO'),
        ('AUTO DE INFRAÇÃO', 'AUTO DE INFRAÇÃO'),
        ('TERMO DE APREENSÃO', 'TERMO DE APREENSÃO'),
        ('COMUNICADO DE DESINTERDIÇÃO', 'COMUNICADO DE DESINTERDIÇÃO'),
        ('TERMO DE INTERDIÇÃO CAUTELAR', 'TERMO DE INTERDIÇÃO CAUTELAR'),
        ('TERMO DE NOTIFICAÇÃO', 'TERMO DE NOTIFICAÇÃO'),
        ('COMPROVANTE DE TAXA', 'COMPROVANTE DE TAXA'),
        ('ALVARÁ DE LOCALIZAÇÃO DA PREFEITURA', 'ALVARÁ DE LOCALIZAÇÃO DA PREFEITURA'),
        ('PLANTA BAIXA', 'PLANTA BAIXA'),
        ('MEMORIAL DESCRITIVO', 'MEMORIAL DESCRITIVO'),
        ('CERTIDÃO DE REGULARIDADE TÉCNICA', 'CERTIDÃO DE REGULARIDADE TÉCNICA'),
        ('MANUAL DE BOAS PRÁTICAS', 'MANUAL DE BOAS PRÁTICAS'),
        ('PROCEDIMENTO OPERACIONAL PADRÃO', 'PROCEDIMENTO OPERACIONAL PADRÃO'),
        ('PLANO DE GERENCIAMENTO DE RESÍDUOS', 'PLANO DE GERENCIAMENTO DE RESÍDUOS'),
        ('AUTORIZAÇÃO DE FUNCIONAMENTO (ANVISA)', 'AUTORIZAÇÃO DE FUNCIONAMENTO (ANVISA)'),
        ('CONTRATO DE TRABALHO', 'CONTRATO DE TRABALHO'),
        ('STATUS DE TRANSMISSÃO (SNGPC)', 'STATUS DE TRANSMISSÃO (SNGPC)'),
        ('IDENTIDADE PROFISSIONAL DO CONSELHO DE CLASSE', 'IDENTIDADE PROFISSIONAL DO CONSELHO DE CLASSE'),
        ('ESCALA DE PLANTÃO DOS PROFISSIONAIS', 'ESCALA DE PLANTÃO DOS PROFISSIONAIS'),
        ('DOCUMENTO DO VEÍCULO', 'DOCUMENTO DO VEÍCULO'),
        ('TREINAMENTO DOS FUNCIONÁRIOS', 'TREINAMENTO DOS FUNCIONÁRIOS'),
        ('CONTRATO DE PRESTAÇÃO DE SERVIÇO', 'CONTRATO DE PRESTAÇÃO DE SERVIÇO'),
        ('RELAÇÃO DOS PROFISSIONAIS CONDUTORES', 'RELAÇÃO DOS PROFISSIONAIS CONDUTORES'),
        ('DOCUMENTO DE HABILITAÇÃO DE CONDUTOR', 'DOCUMENTO DE HABILITAÇÃO DE CONDUTOR'),
        ('CADASTRO NACIONAL DOS ESTABELECIMENTOS DE SAÚDE (CNES)', 'CADASTRO NACIONAL DOS ESTABELECIMENTOS DE SAÚDE (CNES)'),
        ('COMPROVANTE DE PROCESSO', 'COMPROVANTE DE PROCESSO'),
        ('OUTRO', 'OUTRO'),
    )
    CodAutenticidade = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    DataHora = models.DateTimeField(auto_now_add=True)
    Assunto = models.CharField(max_length=100, choices=ASSUNTO_CHOICES)
    Arquivo = models.FileField(upload_to=user_directory_path)
    Descricao = models.TextField(blank=True)
    Processo = models.ForeignKey(Processo)

    def __unicode__(self):
        return unicode(self.DataHora)+' - '+self.Assunto+' ('+self.Descricao+')'

class Setor(models.Model):
    Nome = models.CharField(max_length=100)
    Sigla = models.CharField(max_length=20)
    Unidade = models.CharField(max_length=100)

    def __unicode__(self):
        return self.Sigla+' - '+self.Unidade

    class Meta:
        verbose_name_plural = 'Setores'

class Processo_Tramita_Setor(models.Model):
    ENVIAR = False
    RECEBER = True
    OPERACAO_CHOICES = (
        (ENVIAR, 'Enviar'),
        (RECEBER, 'Receber'),
    )
    Processo = models.ForeignKey(Processo)
    Setor = models.ForeignKey(Setor)
    Operacao = models.BooleanField('Operação', choices=OPERACAO_CHOICES)
    DataHora = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.Operacao == 0:
            return unicode(self.Processo)+' => '+unicode(self.Setor)
        elif self.Operacao == 1:
            return unicode(self.Processo)+' <= '+unicode(self.Setor)

    class Meta:
        verbose_name = 'Tramitação de Processo'
        verbose_name_plural = 'Tramitação de Processos'

class Redesim(models.Model):
    Sigla = models.CharField(max_length=4)
    CNPJ = models.CharField(max_length=14)
    NIRE = models.CharField(max_length=12)
    XML = models.TextField()

class Valor_UFR(models.Model):
    Data = models.DateField()
    Valor = models.FloatField()

    def __unicode__(self):
        return unicode(self.Data)+' - '+unicode(self.Valor)

    class Meta:
        verbose_name = 'Valor da UFR'
        verbose_name_plural = 'Valores da UFR'
