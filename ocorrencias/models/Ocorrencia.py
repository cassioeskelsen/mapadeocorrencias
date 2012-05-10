# -*- coding: utf-8 -*-
from __future__ import division
from django.contrib.gis.db import models
from calendar import datetime
from django.db import *
from ocorrencias.helpers import dictfetchall
import simplejson as json
from decimal import *
from logradouro import  Logradouro
from tipo_ocorrencia import TipoOcorrencia
from localizacao import Localizacao

__author__ = "Cassio Rogerio Eskelsen"
__copyright__ = "Copyright 2012, Cassio Rogerio Eskelsen"
__credits__ = ["Justin Palmer"]
__license__ = "GPL v3"
__version__ = "1.0"
__maintainer__ = "Cassio Rogerio Eskelsen"
__email__ = "eskelsen at gmail.com"
__status__ = "Development"

class Ocorrencia(models.Model):

    numero = models.IntegerField()
    data = models.DateTimeField()
    tipo = models.ForeignKey(TipoOcorrencia)
    local = models.ForeignKey(Localizacao)

    class Meta:
        db_table = 'ocorrencias_ocorrencia'

    def ultimas_ocorrencias(self, qt=200):
        '''Retorna as x ultimas ocorrencias'''
        return Ocorrencia.objects.filter(local__isnull=False).\
            filter(tipo__pode_listar=True).order_by("-data")[:qt]

    def ocorrencias_de_um_tipo(self, tipoOcorrencia):
        '''Retorna todas as ocorrencias de um tipo'''
        return Ocorrencia.objects.filter(
            tipo=tipoOcorrencia).order_by("-data")

    def __init__(self, *args, **kwargs):
        super(Ocorrencia, self).__init__(*args, **kwargs)

    def data_formatada(self):
        return self.data.strftime("%d/%m/%Y %H:%M")

    def eh_luz_do_dia(self):
        return self.data.hour >= 6 and self.data.hour <= 18


class OcorrenciaDTO:
    ''''DTO por falta de criativade para dar outro nome :P '''
    id = 0
    data = None
    endereco = ''
    code = ''
    bairro_id = 0
    lat = 0
    long = 0
