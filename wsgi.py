import os
import sys

root_www = '/mnt/bd1/gis_projects/'

#diretório um nível acima do diretório "mapadeocorrencias"
sys.path.append(root_www)
sys.path.append(os.path.join(root_www, 'mapadeocorrencias'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'mapadeocorrencias.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
