# -*- coding: utf-8 -*-
from __future__ import division
from django.contrib.gis.db import models
from calendar import datetime
from django.db import *
from ocorrencias.helpers import dictfetchall
import simplejson as json

__author__ = "Cassio Rogerio Eskelsen"
__copyright__ = "Copyright 2012, Cassio Rogerio Eskelsen"
__credits__ = ["Justin Palmer"]
__license__ = "GPL v3"
__version__ = "1.0"
__maintainer__ = "Cassio Rogerio Eskelsen"
__email__ = "eskelsen at gmail.com"
__status__ = "Development"

class Bairro(models.Model):
    nome = models.CharField(max_length=50)
    polygon4326 = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'ocorrencias_bairro'

    def __init__(self, *args, **kwargs):
        super(Bairro, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.nome

    def ultimas_ocorrencias_geoJSONcollection(self):
        query = "select ocorrencia.id,ocorrencia.data,tipo.sigla,"\
                "tipo.codigo as codigo,tipo.id as tipo_id,"\
                "logradouro.nome as nomelogradouro,localizacao.numero as nro,"\
                "st_asgeojson(localizacao.posicao_wgs84) as geojson "\
                " from ocorrencias_ocorrencia ocorrencia "\
                "inner join ocorrencias_localizacao localizacao on " \
                    "(localizacao.id=ocorrencia.local_id) "\
                "inner join ocorrencias_logradouro logradouro on " \
                    "(logradouro.id=localizacao.logradouro_id) "\
                "inner join ocorrencias_tipoocorrencia tipo on " \
                    "(tipo.id=ocorrencia.tipo_id) "\
                "inner join ocorrencias_naturezatipoocorrencia natureza on "\
                    "(natureza.id=natureza_id), ocorrencias_bairro bairro "\
                "where ST_Contains(bairro.polygon4326," \
                "localizacao.posicao_wgs84) "\
                "and tipo.pode_listar=true "\
                "and extract(year from data) in (" + \
                str(datetime.date.today().year - 1) + \
                "," + str(datetime.date.today().year) + ") "\
                "and bairro.id= " + str(self.id)
        cursor = connection.cursor()
        cursor.execute(query)
        retorno = dictfetchall(cursor)
        connection.close()
        features = []
        for ocorrencia in retorno:
            prop = dict(id=ocorrencia['id'],
                reportado=ocorrencia['data'].strftime("%d/%m/%Y %H:%M"),
                endereco=ocorrencia['nomelogradouro'] + ', ' +
                            str(ocorrencia['nro']),
                code=ocorrencia['sigla'],
                tipo=ocorrencia['tipo_id'],
                codigo=ocorrencia['codigo']
            )
            geom = json.loads(ocorrencia['geojson'])
            features.append(dict(id=ocorrencia['id'], type="Feature",
                properties=prop, geometry=geom))
        return features

    def lista_bairros_geoJSONcollection(self, idBairro=None):
        query = "select id, " \
                "ST_AsGeoJSON(GeometryN(polygon4326,1)) as geojson" \
                " from ocorrencias_bairro"
        if not idBairro is None:
            query += " where id=" + str(idBairro)
        cursor = connection.cursor()
        cursor.execute(query)
        retorno = dictfetchall(cursor)
        connection.close()
        features = []
        for bairro in retorno:
            geom = json.loads(bairro['geojson'])
            features.append(dict(id=bairro['id'], type="Polygon",
                properties=dict(permalink=bairro['id']), geometry=geom))
        return dict(type="FeatureCollection", features=features)

    def ocorrencias_por_bairros(self):
        query = "select bairro.id, bairro.nome, count(*)  as qtocorrencias "\
                " from ocorrencias_ocorrencia ocorrencia "\
                " inner join ocorrencias_tipoocorrencia tipo on " \
                "(tipo.id=ocorrencia.tipo_id) "\
                " inner join ocorrencias_localizacao localizacao on " \
                "(localizacao.id=ocorrencia.local_id) , " \
                "ocorrencias_bairro bairro "\
                " where ST_Contains(bairro.polygon4326," \
                "localizacao.posicao_wgs84) "\
                " and tipo.pode_listar=true "\
                " group by bairro.id, bairro.nome "\
                " order by bairro.nome"
        cursor = connection.cursor()
        cursor.execute(query)
        retorno = dictfetchall(cursor)
        connection.close()
        return retorno

    def comparativo_ocorrencias_bairro(self):
        query = "select bairro.id, bairro.nome,tipo.codigo as codigo ," \
                "tipo.nome_para_listagem, extract(year from data) as ano, " \
                "count(*)   as qtocorrencias " \
                " from ocorrencias_ocorrencia ocorrencia "\
                " inner join ocorrencias_tipoocorrencia tipo on " \
                    "(tipo.id=ocorrencia.tipo_id) "\
                " inner join ocorrencias_localizacao localizacao on "\
                    "(localizacao.id=ocorrencia.local_id) , "\
                    "ocorrencias_bairro bairro "\
                " where ST_Contains(bairro.polygon4326,"\
                "localizacao.posicao_wgs84) "\
                " and tipo.pode_listar=true "\
                " and bairro.id=" + str(self.id) + \
                " and extract(year from data) in (" + \
                    str(datetime.date.today().year - 1) + "," + \
                    str(datetime.date.today().year) + ") " \
                " group by bairro.id, bairro.nome,tipo.codigo," \
                "tipo.nome_para_listagem ,extract(year from data) "\
                " order by nome_para_listagem"

        cursor = connection.cursor()
        cursor.execute(query)
        retorno = dictfetchall(cursor)
        connection.close()
        lista = dict()
        for linha in retorno:
            if linha['ano'] == datetime.date.today().year:
                if lista.keys().__contains__(linha['codigo']):
                    lista[linha['codigo']].update(dict(lista[linha['codigo']],
                        corrente=linha['qtocorrencias'],
                        diferenca=self.__calculaDiferenca__(lista[linha['codigo']]['anterior'],
                            linha['qtocorrencias'])))
                else:
                    lista[linha['codigo']] = dict(nome=linha['nome_para_listagem'],
                        id=linha['codigo'],
                        corrente=linha['qtocorrencias'],
                        anterior=0, diferenca=100)
            else:
                if lista.keys().__contains__(linha['codigo']):
                    lista[linha['codigo']].update(
                        dict(lista[linha['codigo']],
                            anterior=linha['qtocorrencias'],
                            diferenca=self.__calculaDiferenca__(linha['qtocorrencias'],
                                lista[linha['codigo']]['anterior'])))
                else:
                    lista[linha['codigo']] = \
                    dict(nome=linha['nome_para_listagem'],
                        id=linha['codigo'],
                        anterior=linha['qtocorrencias'],
                        corrente=0,
                        diferenca=-100)

        return lista

    def comparativo_por_natureza(self):
        query = " select bairro.id, bairro.nome,natureza.id as idnatureza, "\
                "natureza.nome as nome_natureza, extract(year from data) as ano,"\
                " count(*)   as qtocorrencias "\
                " from ocorrencias_ocorrencia ocorrencia  "\
                " inner join ocorrencias_localizacao localizacao on "\
                    "(localizacao.id=ocorrencia.local_id)  "\
                " inner join ocorrencias_tipoocorrencia tipo on "\
                    "(tipo.id=ocorrencia.tipo_id)  "\
                " inner join ocorrencias_naturezatipoocorrencia natureza on "\
                    "(natureza.id=natureza_id), ocorrencias_bairro bairro  "\
                " where ST_Contains(bairro.polygon4326,localizacao.posicao_wgs84)  "\
                " and tipo.pode_listar=true  "\
                " and bairro.id=" + str(self.id) + \
                " and extract(year from data) in (" + \
                str(datetime.date.today().year - 1) + \
                "," + \
                str(datetime.date.today().year) + ") "\
                " group by bairro.id, bairro.nome,natureza.id,"\
                "natureza.nome,extract(year from data)"

        cursor = connection.cursor()
        cursor.execute(query)
        retorno = dictfetchall(cursor)
        connection.close()
        lista = dict()
        for linha in retorno:
            if linha['ano'] == datetime.date.today().year:
                if lista.keys().__contains__(linha['idnatureza']):
                    lista[linha['idnatureza']].update(
                        dict(lista[linha['idnatureza']],
                            corrente=linha['qtocorrencias'],
                            diferenca=self.__calculaDiferenca__(lista[linha['idnatureza']]['anterior'],
                                linha['qtocorrencias'])))
                else:
                    lista[linha['idnatureza']] = \
                    dict(nome=linha['nome_natureza'],
                        id=linha['idnatureza'],
                        corrente=linha['qtocorrencias'],
                        anterior=0, diferenca=100)
            else:
                if lista.keys().__contains__(linha['idnatureza']):
                    lista[linha['idnatureza']].update(
                        dict(lista[linha['idnatureza']],
                            anterior=linha['qtocorrencias'],
                            diferenca=self.__calculaDiferenca__(linha['qtocorrencias'],
                                lista[linha['idnatureza']]['anterior'])))
                else:
                    lista[linha['idnatureza']] = \
                    dict(nome=linha['nome_natureza'],
                        id=linha['idnatureza'],
                        anterior=linha['qtocorrencias'],
                        corrente=0,
                        diferenca=-100)

        return lista

    def __calculaDiferenca__(self, anterior, corrente):
        if anterior <= 0:
            return 100
        return round(corrente * 100 / anterior - 100, 2)

    def retorna_total_ocorrencias_bairro(self, tipo_id):
        query = "select bairro.id, bairro.nome, count(*) as total "\
                " from ocorrencias_ocorrencia ocor "\
                " inner join ocorrencias_localizacao as local on " \
                "local.id=ocor.local_id, ocorrencias_bairro as bairro "\
                " where st_contains(bairro.polygon4326,local.posicao_wgs84)"
        if not tipo_id is None:
            query = query + " and tipo_id=" + str(tipo_id)
        query += "group by bairro.id, bairro.nome order by total desc"
        cursor = connection.cursor()
        cursor.execute(query)
        retorno = dictfetchall(cursor)
        connection.close()
        return retorno
