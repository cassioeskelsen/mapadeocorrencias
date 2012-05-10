# -*- coding: utf-8 -*-
from __future__ import division
from django.contrib.gis.db import models
from django.db import *
from decimal import *

__author__ = "Cassio Rogerio Eskelsen"
__copyright__ = "Copyright 2012, Cassio Rogerio Eskelsen"
__credits__ = ["Justin Palmer"]
__license__ = "GPL v3"
__version__ = "1.0"
__maintainer__ = "Cassio Rogerio Eskelsen"
__email__ = "eskelsen at gmail.com"
__status__ = "Development"

class NaturezaTipoOcorrencia(models.Model):
    '''
    Define o tipo da ocorrência: Violenta, Não Violenta, Sexual, etc
    '''
    nome = models.CharField(max_length=30)

    class Meta:
        db_table = 'ocorrencias_naturezatipoocorrencia'

    def __init__(self, *args, **kwargs):
        super(NaturezaTipoOcorrencia, self).__init__(*args, **kwargs)

    def ListagemParaSite(self):
        return NaturezaTipoOcorrencia.objects.all()

    def __unicode__(self):
        return self.nome
