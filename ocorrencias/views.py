from django.http import HttpResponse
from django.contrib.gis.db import models
from django.shortcuts import render_to_response
from django.contrib.gis.shortcuts import *
from ocorrencias.models import *
from django.db import *
from django.template import Context, loader
from ocorrencias.helpers import *
from django.db.models import Max, Min
from itertools import *
import simplejson as json

__author__ = "Cassio Rogerio Eskelsen"
__copyright__ = "Copyright 2012, Cassio Rogerio Eskelsen"
__credits__ = ["Justin Palmer"]
__license__ = "GPL v3"
__version__ = "1.0"
__maintainer__ = "Cassio Rogerio Eskelsen"
__email__ = "eskelsen at gmail.com"
__status__ = "Development"

def retorna_estatistica(tipo_id=None):
    periodo, retorno = EstatisticaOcorrencias().get_estatistica(tipo_id)
    connection.close()
    tipos = []
    ocorrencias = []
    for k, g in groupby([x.values()[0] for x in retorno]):
        tipos.append(k)

    for tipo in tipos:
        totalDoTipo = 0
        est = EstatisticaOcorrencias()
        for d in ifilter(lambda x: x['codigo'] == tipo, retorno):
            totalDoTipo += d['total']
            est.nome_ocorrencia = d['nome']
            #regra para o dia "normal"
            if d['hora'] >= 5 and d['hora'] <= 18:
                est.qtOcorrenciasDiurnas += d['total']
            else:
                est.qtOcorrenciasNoturnas += d['total']
            #regra para fim de semana
            if (d['diadasemana'] in [5, 6] and d['hora'] >= 20) \
                or (d['diadasemana'] in [6, 0] and d['hora'] <= 2):
                est.qtOcorrenciasFimDeSemana += d['total']
        est.qtTotalOcorrencias = totalDoTipo
        ocorrencias.append(est)

    return ocorrencias, periodo


def calcula_qt_ocorrencias_bairro(tipo_id=None):
    return Bairro().retorna_total_ocorrencias_bairro(tipo_id)


def indexEstatistica(request):
    ocorrencias, periodo = retorna_estatistica()
    t = loader.get_template('estatisticas/index.html')
    c = Context({
        'estatisticaOcorrencias': ocorrencias,
        'periodo': periodo,
        'data_path': "trends-index"
    })
    return HttpResponse(t.render(c))


def estatisticaJson(request):
    listao = EstatisticaOcorrencias().retorna_estatistica_semanal()
    return HttpResponse(json.dumps(listao), mimetype="application/octet-stream")


def indexCrimes(request):
    min_max = Ocorrencia.objects.aggregate(Max('data'), Min('data'))
    periodo = 'De ' + min_max['data__min'].strftime("%d/%m/%Y") + ' a ' + min_max['data__max'].strftime("%d/%m/%Y")
    t = loader.get_template('crimes/index.html')
    c = Context({
        'periodo': periodo,
        'data_path': "crimes-index",
        'naturezas': NaturezaTipoOcorrencia().ListagemParaSite(),
        'tipos': TipoOcorrencia().ListagemParaSite()
    })
    return HttpResponse(t.render(c))


def ocorrenciasJson(request):
    features = []
    for ocorrencia in Ocorrencia().ultimas_ocorrencias():

        prop = dict(id=ocorrencia.id,
                    reportado=ocorrencia.data.strftime("%d/%m/%Y %H:%M"),
                    endereco=ocorrencia.local.logradouro.nome + ', ' + str(ocorrencia.local.numero),
                    code=ocorrencia.tipo.sigla,
                    tipo=ocorrencia.tipo_id,
                    codigo=ocorrencia.tipo.codigo
                    )
        geom = dict(type="Point",
                    coordinates=[ocorrencia.local.posicao_wgs84.x,
                                 ocorrencia.local.posicao_wgs84.y])
        features.append(dict(id=ocorrencia.id,
                            type="Feature",
                            properties=prop,
                            geometry=geom))

    diczao = dict(type="FeatureCollection", features=features)
    return HttpResponse(json.dumps(diczao), mimetype="application/octet-stream")


def ocorrenciasBairroJSON(request, codigoBairro):
    bairro = Bairro.objects.get(id=codigoBairro)
    diczao = dict(type="FeatureCollection", features=bairro.ultimas_ocorrencias_geoJSONcollection())
    return HttpResponse(json.dumps(diczao), mimetype="application/octet-stream")


def showDelito(request, codigoDelito):

    tipo = TipoOcorrencia.objects.get(codigo=codigoDelito)

    ocorrencias, periodo = retorna_estatistica(tipo.id)

    maxmax = Ocorrencia.objects.filter(tipo=tipo).aggregate(Max('data'))

    #pega os 5 bairros + agitados
    qtPorBairros = filter(lambda x: x['total'] > 1, calcula_qt_ocorrencias_bairro(tipo.id))[:5]

    t = loader.get_template("delito/show.html")
    c = Context({
        'tipo': tipo,
        'dados': ocorrencias[0],
        'bairrosRecorrentes': qtPorBairros,
        'periodo': periodo,
        'ultima_ocorrencia': maxmax['data__max'].strftime("%d/%m/%Y"),
        'data_path': "delitos-show",
    })
    return HttpResponse(t.render(c))


def delitoJson(request, codigoDelito):
    tipo = TipoOcorrencia.objects.get(codigo=codigoDelito)
    return HttpResponse(json.dumps(dict(codigo=tipo.codigo,
                                        nome=tipo.nome_para_listagem)),
                                        mimetype="application/json")


def delitoGeoJson(request, codigoDelito):
    features = []
    tipo = TipoOcorrencia.objects.get(codigo=codigoDelito)
    for ocorrencia in Ocorrencia().ocorrencias_de_um_tipo(tipo):

        prop = dict(id=ocorrencia.id,
                    reportado="%02d-%02d-%02dT%02d:%02d:00Z" %
                               (ocorrencia.data.year,
                                ocorrencia.data.month,
                                ocorrencia.data.day,
                                ocorrencia.data.hour,
                                ocorrencia.data.minute),
                    endereco=ocorrencia.local.logradouro.nome + ', ' +
                             str(ocorrencia.local.numero),
                    code=ocorrencia.tipo.sigla,
                    tipo=ocorrencia.tipo_id,
                    codigo=ocorrencia.tipo.codigo
                    )
        geom = dict(type="Point",
                coordinates=[ocorrencia.local.posicao_wgs84.x,
                             ocorrencia.local.posicao_wgs84.y])
        features.append(dict(id=ocorrencia.id,
                        type="Feature",
                        properties=prop,
                        geometry=geom))

    diczao = dict(type="FeatureCollection", features=features)
    return HttpResponse(json.dumps(diczao), mimetype="application/octet-stream")


def historicoDelitoJson(request, codigoDelito):
    historico = TipoOcorrencia().retorna_historico_de_delito(codigoDelito)
    return HttpResponse(json.dumps(historico), mimetype="application/json")


def indexBairros(request):
    bairrosLista = []
    letras = dict()
    for bairro in Bairro().ocorrencias_por_bairros():
        letras[asciize(bairro['nome'])[0:1]] = ' '
        bairrosLista.append(
            dict(id=bairro['id'],
                 nome=bairro['nome'],
                 qtocorrencias=bairro['qtocorrencias'],
                 letra=asciize(bairro['nome'])[0:1]))
    t = loader.get_template('bairros/index.html')
    c = Context({
        'data_path': "bairros-index",
        'bairros': bairrosLista,
        'letras': sorted(letras.keys())
    })
    return HttpResponse(t.render(c))


def bairrosJson(request):
    bairros = Bairro().lista_bairros_geoJSONcollection()
    return HttpResponse(json.dumps(bairros), mimetype="application/octet-stream")


def bairroJson(request, idBairro):
    bairros = Bairro().lista_bairros_geoJSONcollection(idBairro)
    return HttpResponse(json.dumps(bairros), mimetype="application/octet-stream")


def showBairro(request, codigoBairro):
    bairro = Bairro.objects.get(id=codigoBairro)
    naturezas = bairro.comparativo_por_natureza()
    somac = 0
    somaa = 0
    somac = sum([value['corrente'] for key, value in naturezas.items()])
    somaa = sum([value['anterior'] for key, value in naturezas.items()])

    t = loader.get_template('bairros/show.html')

    c = Context({
        'data_path': 'bairro-show',
        'bairro': bairro,
        'comparacao_ano': bairro.comparativo_ocorrencias_bairro(),
        'comparacao_natureza': naturezas,
        'soma_anterior': somaa,
        'soma_atual': somac,
        'ano_anterior': datetime.date.today().year - 1,
        'ano_atual': datetime.date.today().year,
        'ultimas': Ocorrencia.objects.filter(tipo__pode_listar=True).order_by('-data')[:5]
    })

    return HttpResponse(t.render(c))
