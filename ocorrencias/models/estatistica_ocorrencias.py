# -*- coding: utf-8 -*-
from __future__ import division
from django.contrib.gis.db import models
from django.contrib.gis.shortcuts import *
from calendar import datetime
from django.db import *
from django.db.models import Max, Min
from ocorrencias.helpers import dictfetchall
import simplejson as json
from decimal import *
from logradouro import  Logradouro
from tipo_ocorrencia import TipoOcorrencia
from localizacao import Localizacao
from ocorrencia import Ocorrencia

__author__ = "Cassio Rogerio Eskelsen"
__copyright__ = "Copyright 2012, Cassio Rogerio Eskelsen"
__credits__ = ["Justin Palmer"]
__license__ = "GPL v3"
__version__ = "1.0"
__maintainer__ = "Cassio Rogerio Eskelsen"
__email__ = "eskelsen at gmail.com"
__status__ = "Development"

class EstatisticaOcorrencias:
    codigo = 0
    nome_ocorrencia = ''
    qtOcorrenciasDiurnas = 0
    qtOcorrenciasNoturnas = 0
    qtOcorrenciasFimDeSemana = 0
    qtTotalOcorrencias = 0

    def PercentualOcorrenciasDiurnas(self):
        if self.qtTotalOcorrencias == 0:
            return 0
        return  round((Decimal(self.qtOcorrenciasDiurnas) /
                       Decimal(self.qtTotalOcorrencias) * 100), 2)

    def PercentualOcorrenciasNoturnas(self):
        if self.qtTotalOcorrencias == 0:
            return 0
        return  round((Decimal(self.qtOcorrenciasNoturnas) /
                       Decimal(self.qtTotalOcorrencias) * 100), 2)

    def PercentualOcorrenciasFimDeSemana(self):
        if self.qtTotalOcorrencias == 0:
            return 0
        return  round((Decimal(self.qtOcorrenciasFimDeSemana) /
                       Decimal(self.qtTotalOcorrencias) * 100), 2)

    def get_estatistica(self, tipo_id=None):
        query = "select count(ocor.id) as total ,tipo.codigo as codigo, \
                tipo.nome_para_listagem as nome, \
                extract(hour from data) as hora , \
                extract (dow from data) as diadasemana \
                from  ocorrencias_ocorrencia as ocor \
                join ocorrencias_tipoocorrencia as tipo \
                on (tipo.id = ocor.tipo_id) \
                where tipo.pode_listar = true "
        if tipo_id != None:
            query = query + " and tipo_id = " + str(tipo_id)
        query += " group by ocor.tipo_id,tipo.codigo, " \
                "tipo.nome_para_listagem,extract(hour from data) , " \
                "extract (dow from data) \
                order by ocor.tipo_id"
        min_max = Ocorrencia.objects.aggregate(Max('data'), Min('data'))
        periodo = 'De ' + min_max['data__min'].strftime("%d/%m/%Y") + \
                  ' a ' + min_max['data__max'].strftime("%d/%m/%Y")
        cursor = connection.cursor()
        cursor.execute(query)
        retorno = dictfetchall(cursor)
        return periodo, retorno

    def retorna_estatistica_semanal(self):
        semanaPrev = []
        semanaCurr = []
        mesPrev = []
        mesCurr = []
        semana = 0
        query = "select count(*), extract(week from data) as semana " \
                "from ocorrencias_ocorrencia \
                where extract(year from data)  = %s \
                group by extract(week from data), extract(year from data) \
                order by  extract(week from data)"
        for ano in range(datetime.date.today().year - 1, datetime.date.today().year + 1):
            ocorrencias = Ocorrencia.objects.filter(data__year=ano).order_by("data").all()
            total = ocorrencias.count() - 1
            i = 0
            dadosSemana = dict()
            dadosMes = dict()

            for ocor in ocorrencias:
                semana = int(ocor.data.strftime("%W"))
                mes = ocor.data.month
                if(semana in dadosSemana.keys()):
                    dadosSemana[semana] += 1
                else:
                    dadosSemana[semana] = 1
                if(mes in dadosMes.keys()):
                    dadosMes[mes] += 1
                else:
                    dadosMes[mes] = 1

                i += 1

            for dad in dadosSemana:
                if ano == datetime.date.today().year - 1:
                    semanaPrev.append(dict(week=dad, value=dadosSemana[dad]))
                else:
                    semanaCurr.append(dict(week=dad, value=dadosSemana[dad]))

            for dad in dadosMes:
                if ano == datetime.date.today().year - 1:
                    mesPrev.append(dict(month=dad, value=dadosMes[dad]))
                else:
                    mesCurr.append(dict(month=dad, value=dadosMes[dad]))
        listSemanas = []
        listSemanas.append(dict(series="prev", values=semanaPrev))
        listSemanas.append(dict(series="curr", values=semanaCurr))
        listMeses = []
        listMeses.append(dict(series="prev", values=mesPrev))
        listMeses.append(dict(series="curr", values=mesCurr))
        listao = [listSemanas, listMeses]
        return listao
