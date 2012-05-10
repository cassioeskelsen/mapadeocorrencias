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

class LogradouroVariacao(models.Model):
    '''
    Especifica variantes dos logradouros
    Esses variantes podem ser nomes alternativos ou cadastrados
    de forma errônea no sistema da PM
    '''

    logradouro = models.ForeignKey(Logradouro)
    variacao = models.CharField(max_length=100)

    class Meta:
        db_table = 'ocorrencias_logradourovariacao'

    def __init__(self, *args, **kwargs):
        super(LogradouroVariacao, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.logradouro.nome + ', ' + \
               str(self.numero) + ', ' + self.logradouro.cidade
