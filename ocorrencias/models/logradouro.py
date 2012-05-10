# -*- coding: utf-8 -*-
from __future__ import division
from django.contrib.gis.db import models

__author__ = "Cassio Rogerio Eskelsen"
__copyright__ = "Copyright 2012, Cassio Rogerio Eskelsen"
__credits__ = ["Justin Palmer"]
__license__ = "GPL v3"
__version__ = "1.0"
__maintainer__ = "Cassio Rogerio Eskelsen"
__email__ = "eskelsen at gmail.com"
__status__ = "Development"

class Logradouro(models.Model):

    tipo = models.CharField(max_length=5)
    nome = models.CharField(max_length=100)
    variacao_pm = models.CharField(max_length=100, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, default='SC', null=True)
    codigo = models.IntegerField(max_length=2)
    codigo = models.IntegerField(max_length=2)

    class Meta:
        db_table = 'ocorrencias_logradouro'

    def __init__(self, *args, **kwargs):
        super(Logradouro, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.nome + ', ' + self.bairro + ', ' + self.cidade
