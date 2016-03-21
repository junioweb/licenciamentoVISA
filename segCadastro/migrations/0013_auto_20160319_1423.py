# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segCadastro', '0012_auto_20160307_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='Assunto',
            field=models.CharField(choices=[(b'AUTORIZA\xc3\x87\xc3\x83O DE FUNCIONAMENTO (AGEVISA)', b'AUTORIZA\xc3\x87\xc3\x83O DE FUNCIONAMENTO (AGEVISA)'), (b'RELAT\xc3\x93RIO T\xc3\x89CNICO DE INSPE\xc3\x87\xc3\x83O', b'RELAT\xc3\x93RIO T\xc3\x89CNICO DE INSPE\xc3\x87\xc3\x83O'), (b'TERMO DE INSPE\xc3\x87\xc3\x83O', b'TERMO DE INSPE\xc3\x87\xc3\x83O'), (b'AUTO DE INFRA\xc3\x87\xc3\x83O', b'AUTO DE INFRA\xc3\x87\xc3\x83O'), (b'TERMO DE APREENS\xc3\x83O', b'TERMO DE APREENS\xc3\x83O'), (b'COMUNICADO DE DESINTERDI\xc3\x87\xc3\x83O', b'COMUNICADO DE DESINTERDI\xc3\x87\xc3\x83O'), (b'TERMO DE INTERDI\xc3\x87\xc3\x83O CAUTELAR', b'TERMO DE INTERDI\xc3\x87\xc3\x83O CAUTELAR'), (b'TERMO DE NOTIFICA\xc3\x87\xc3\x83O', b'TERMO DE NOTIFICA\xc3\x87\xc3\x83O'), (b'COMPROVANTE DE TAXA', b'COMPROVANTE DE TAXA'), (b'ALVAR\xc3\x81 DE LOCALIZA\xc3\x87\xc3\x83O DA PREFEITURA', b'ALVAR\xc3\x81 DE LOCALIZA\xc3\x87\xc3\x83O DA PREFEITURA'), (b'PLANTA BAIXA', b'PLANTA BAIXA'), (b'MEMORIAL DESCRITIVO', b'MEMORIAL DESCRITIVO'), (b'CERTID\xc3\x83O DE REGULARIDADE T\xc3\x89CNICA', b'CERTID\xc3\x83O DE REGULARIDADE T\xc3\x89CNICA'), (b'MANUAL DE BOAS PR\xc3\x81TICAS', b'MANUAL DE BOAS PR\xc3\x81TICAS'), (b'PROCEDIMENTO OPERACIONAL PADR\xc3\x83O', b'PROCEDIMENTO OPERACIONAL PADR\xc3\x83O'), (b'PLANO DE GERENCIAMENTO DE RES\xc3\x8dDUOS', b'PLANO DE GERENCIAMENTO DE RES\xc3\x8dDUOS'), (b'AUTORIZA\xc3\x87\xc3\x83O DE FUNCIONAMENTO (ANVISA)', b'AUTORIZA\xc3\x87\xc3\x83O DE FUNCIONAMENTO (ANVISA)'), (b'CONTRATO DE TRABALHO', b'CONTRATO DE TRABALHO'), (b'STATUS DE TRANSMISS\xc3\x83O (SNGPC)', b'STATUS DE TRANSMISS\xc3\x83O (SNGPC)'), (b'IDENTIDADE PROFISSIONAL DO CONSELHO DE CLASSE', b'IDENTIDADE PROFISSIONAL DO CONSELHO DE CLASSE'), (b'ESCALA DE PLANT\xc3\x83O DOS PROFISSIONAIS', b'ESCALA DE PLANT\xc3\x83O DOS PROFISSIONAIS'), (b'DOCUMENTO DO VE\xc3\x8dCULO', b'DOCUMENTO DO VE\xc3\x8dCULO'), (b'TREINAMENTO DOS FUNCION\xc3\x81RIOS', b'TREINAMENTO DOS FUNCION\xc3\x81RIOS'), (b'CONTRATO DE PRESTA\xc3\x87\xc3\x83O DE SERVI\xc3\x87O', b'CONTRATO DE PRESTA\xc3\x87\xc3\x83O DE SERVI\xc3\x87O'), (b'RELA\xc3\x87\xc3\x83O DOS PROFISSIONAIS CONDUTORES', b'RELA\xc3\x87\xc3\x83O DOS PROFISSIONAIS CONDUTORES'), (b'DOCUMENTO DE HABILITA\xc3\x87\xc3\x83O DE CONDUTOR', b'DOCUMENTO DE HABILITA\xc3\x87\xc3\x83O DE CONDUTOR'), (b'CADASTRO NACIONAL DOS ESTABELECIMENTOS DE SA\xc3\x9aDE (CNES)', b'CADASTRO NACIONAL DOS ESTABELECIMENTOS DE SA\xc3\x9aDE (CNES)'), (b'COMPROVANTE DE PROCESSO', b'COMPROVANTE DE PROCESSO'), (b'OUTRO', b'OUTRO')], max_length=100),
        ),
        migrations.AlterField(
            model_name='documento',
            name='Descricao',
            field=models.TextField(blank=True),
        ),
    ]
