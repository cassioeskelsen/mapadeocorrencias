# -*- coding: utf-8 -*-
from __future__ import division
from django.contrib.gis.db import models
from django.db import *
from decimal import *
from logradouro import Logradouro

__author__ = "Cassio Rogerio Eskelsen"
__copyright__ = "Copyright 2012, Cassio Rogerio Eskelsen"
__credits__ = ["Justin Palmer"]
__license__ = "GPL v3"
__version__ = "1.0"
__maintainer__ = "Cassio Rogerio Eskelsen"
__email__ = "eskelsen at gmail.com"
__status__ = "Development"

class Localizacao(models.Model):
    '''
    Define a posicao de um determinado endereco (numero de porta, por exemplo)
    '''
    latitude_wgs84 = models.FloatField(null=True)
    longitude_wgs84 = models.FloatField(null=True)
    posicao_wgs84 = models.PointField(null=True)
    #posicao = 0 nao processado,1 encontrado, 2 nao encontrado
    posicao_status = models.IntegerField(default=0)
    logradouro = models.ForeignKey(Logradouro)
    numero = models.IntegerField(default=0)
    objects = models.GeoManager()

    class Meta:
        db_table = 'ocorrencias_localizacao'

    def __init__(self, *args, **kwargs):
        super(Localizacao, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.posicao_wgs84
