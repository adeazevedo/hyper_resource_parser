import requests
from time import sleep
#servidor = ''
servidor = 'http://LUC00557347.ibge.gov.br/'
arr_get_for_collection = [
'controle-list/gasto-list/countresource',
'controle-list/gasto-list/offsetlimit/1&10',
'controle-list/gasto-list/groupbycount/tipo_gasto',
'controle-list/gasto-list/filter/tipo_gasto/eq/3',
'ibge/bcim/unidades-federativas/filter/geom/within/' + servidor + 'ibge/bcim/municipios/3159407/geom/*',
'ibge/bcim/unidades-federativas/?*contains=POINT(-42 -21)',
'ibge/bcim/unidades-federativas/?*contains=POINT(-42 -21)&sigla=RJ',
'ibge/bcim/unidades-federativas/?*contains=URL&sigla=RJ',
'ibge/bcim/unidades-federativas/contains/POINT(-42 -21)',
'ibge/bcim/aldeias-indigenas/within/POLYGON((-41.8 -21.2,-41.8 -17.8,-28.8 -17.8,-28.8 -21.,-41.8 -21.2))/',
'ibge/bcim/aldeias-indigenas/within/' + servidor + 'ibge/bcim/unidades-federativas/ES/*',
'ibge/bcim/aldeias-indigenas/within/' + servidor + 'ibge/bcim/unidades-federativas/PA/*',
'ibge/bcim/unidades-federativas/filter/sigla/in/ES,PA/',
'ibge/bcim/aldeias-indigenas/within/' + servidor +  'ibge/bcim/unidades-federativas/ES/*or/within/' + servidor + 'ibge/bcim/unidades-federativas/PA/*',
'ibge/bcim/aldeias-indigenas/filter/geom/within/' + servidor + 'ibge/bcim/unidades-federativas/ES/*or/geom/within/' + servidor + 'ibge/bcim/unidades-federativas/PA/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + servidor + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + servidor + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + servidor + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + servidor + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + servidor + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + servidor + 'ibge/bcim/unidades-federativas/ES/geom/*or/' + servidor + 'ibge/bcim/unidades-federativas/PR/*',
'ibge/bcim/municipios/within/{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}',
'ibge/bcim/municipios/within/'+ servidor + 'ibge/bcim/unidades-federativas/ES/*',
'ibge/bcim/municipios/filter/geom/overlaps/' + servidor +'ibge/bcim/unidades-federativas/ES/*or/geom/within/' + servidor +'ibge/bcim/unidades-federativas/ES/*and/geocodigo/startswith/32/'
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






