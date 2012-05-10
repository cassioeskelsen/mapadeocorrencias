# -*- coding: utf-8 -*-
from __future__ import division
from django.contrib.gis.db import models
from calendar import datetime
from django.db import *
from ocorrencias.helpers import dictfetchall
import simplejson as json
from decimal import *
from natureza_tipo_ocorrencia import NaturezaTipoOcorrencia

__author__ = "Cassio Rogerio Eskelsen"
__copyright__ = "Copyright 2012, Cassio Rogerio Eskelsen"
__credits__ = ["Justin Palmer"]
__license__ = "GPL v3"
__version__ = "1.0"
__maintainer__ = "Cassio Rogerio Eskelsen"
__email__ = "eskelsen at gmail.com"
__status__ = "Development"

class TipoOcorrencia(models.Model):
    codigo = models.CharField(max_length=5)
    nome_ocorrencia = models.CharField(max_length=100)
    nome_para_listagem = models.CharField(max_length=100)
    pode_listar = models.BooleanField(default=True)
    natureza = models.ForeignKey(NaturezaTipoOcorrencia)
    sigla = models.CharField(max_length=2)

    class Meta:
        db_table = 'ocorrencias_tipoocorrencia'

    def ListagemParaSite(self):
        return TipoOcorrencia.objects.filter(pode_listar=True).all()

    def __unicode__(self):
        return self.nome_ocorrencia

    def retorna_historico_de_delito(self, codigoDelito):
        tipo = TipoOcorrencia.objects.get(codigo=codigoDelito)
        query = "select extract (month from data) as mes, "\
                "extract(year from data) as ano, count(*) "\
                " from ocorrencias_ocorrencia "\
                " where tipo_id = " + str(tipo.id) +\
                " and data::date > (now()::date - 1080)"\
                " group by extract (month from data), extract(year from data) "\
                " order by ano,mes"
        cursor = connection.cursor()
        cursor.execute(query)
        retorno = dictfetchall(cursor)
        connection.close()
        historico = []
        for ocor in retorno:
            data = str(ocor['ano']) + '-' + '{:*>2}'.format(str(ocor['mes']))\
                   + '-01' + 'T' + '00:00:00-07:00'
            data = "%02d-%02d-01T00:00:00-07:00" % (ocor['ano'], ocor['mes'])
            historico.append(dict(count=int(ocor['count']), date=data))
        return historico
