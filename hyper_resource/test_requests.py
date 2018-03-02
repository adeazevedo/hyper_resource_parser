import requests
from time import sleep
#servidor = 'http://luc00557347.ibge.gov.br/'
servidor = 'http://LUC00557196.ibge.gov.br:8080/'
arr_get_for_collection = [
'controle-list/gasto-list/countresource',
'controle-list/gasto-list/offsetlimit/1&10',
'controle-list/gasto-list/groupbycount/tipo_gasto',
'controle-list/gasto-list/filter/tipo_gasto/eq/3',
'ibge/bcim/unidades-federativas/filter/geom/within/ibge/bcim/municipios/3159407/geom*'
'ibge/ibge/bcim/unidades-federativas/?*contains=POINT(-42 -21)',
'ibge/bcim/unidades-federativas/?*contains=POINT(-42 -21)&sigla=RJ',
'ibge/bcim/unidades-federativas/?*contains=URL&sigla=RJ',
'ibge/bcim/unidades-federativas/contains/POINT(-42 -21)',
'ibge/bcim/aldeias-indigenas/within/POLYGON((-41.8 -21.2,-41.8 -17.8,-28.8 -17.8,-28.8 -21.,-41.8 -21.2))/',
'ibge/bcim/aldeias-indigenas/within/http://127.0.0.1:8001/ibge/bcim/unidades-federativas/ES',
'ibge/bcim/aldeias-indigenas/within/http://127.0.0.1:8001/ibge/bcim/unidades-federativas/PA/',
'ibge/bcim/unidades-federativas/filter/sigla/in/ES,PA/',
'ibge/bcim/aldeias-indigenas/within/ibge/bcim/unidades-federativas/ES/*or/within/ibge/bcim/unidades-federativas/PA/',
'ibge/bcim/aldeias-indigenas/filter/geom/within/ibge/bcim/unidades-federativas/ES/*or/geom/within/ibge/bcim/unidades-federativas/PA/',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/ibge/bcim/unidades-federativas/ES/geom/*',
'http://luc00557347.ibge.gov.bribge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/http://luc00557347.ibge.gov.bribge/bcim/unidades-federativas/ES/geom/*',
'http://luc00557347.ibge.gov.bribge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/http://luc00557347.ibge.gov.bribge/bcim/unidades-federativas/ES/geom/*',
'http://luc00557347.ibge.gov.bribge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/http://luc00557347.ibge.gov.bribge/bcim/unidades-federativas/ES/geom/*',
'http://luc00557347.ibge.gov.bribge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/http://luc00557347.ibge.gov.bribge/bcim/unidades-federativas/ES/geom/*',
'http://luc00557347.ibge.gov.bribge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/http://luc00557347.ibge.gov.bribge/bcim/unidades-federativas/ES/geom/*or/http://luc00557347.ibge.gov.bribge/bcim/unidades-federativas/PR/*',
'http://luc00557347.ibge.gov.bribge/bcim/municipios/within/{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}'
'http://luc00557347.ibge.gov.bribge/bcim/municipios/within/http://luc00557347.ibge.gov.bribge/bcim/unidades-federativas/ES/',
'http://luc00557347.ibge.gov.bribge/bcim/municipios/filter/geom/overlaps/http://luc00557347.ibge.gov.bribge/bcim/unidades-federativas/ES/*or/geom/within/http://luc00557347.ibge.gov.bribge/bcim/unidades-federativas/ES/*and/geocodigo/startswith/32/'
]
requests_with_error = []

for req_str in arr_get_for_collection:

    print('Executing: ' + req_str)
    res = requests.get(servidor + req_str)
    if res.status_code not in (200, 201,202,203,204,300,301,302,303):
        print('Failed: ' + req_str)
        requests_with_error.append(req_str)
if len(requests_with_error) > 1:
    print("***************The urls below failed****************")
    for req_str_error in requests_with_error:
        print(req_str_error)
    print("***************failed urls****************")
else:
    print("*********Sucess***********")






