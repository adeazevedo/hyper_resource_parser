import requests
from time import sleep
#servidor = ''
#servidor = 'http://LUC00557347.ibge.gov.br/'
#SERVER = 'http://LUC00557196.ibge.gov.br:8000/'
#SERVER = "http://172.30.10.130:8000/"
SERVER = "http://172.30.10.86:8800/"
arr_get_for_collection = [
'controle-list/gasto-list/count_resource',
'controle-list/gasto-list/offset_limit/1&10',
'controle-list/gasto-list/group_by_count/tipo_gasto',
'controle-list/gasto-list/filter/tipo_gasto/eq/3',
'ibge/bcim/unidades-federativas/filter/geom/within/' + SERVER + 'ibge/bcim/municipios/3159407/geom/*',
'ibge/bcim/unidades-federativas/?*contains=POINT(-42 -21)',
'ibge/bcim/unidades-federativas/?*contains=POINT(-42 -21)&sigla=RJ',
'ibge/bcim/unidades-federativas/?*contains=URL&sigla=RJ',
'ibge/bcim/unidades-federativas/contains/POINT(-42 -21)',
'ibge/bcim/aldeias-indigenas/within/POLYGON((-41.8 -21.2,-41.8 -17.8,-28.8 -17.8,-28.8 -21.,-41.8 -21.2))/',
'ibge/bcim/aldeias-indigenas/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/*',
'ibge/bcim/aldeias-indigenas/within/' + SERVER + 'ibge/bcim/unidades-federativas/PA/*',
'ibge/bcim/unidades-federativas/filter/sigla/in/ES,PA/',
'ibge/bcim/aldeias-indigenas/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/*or/within/' + SERVER + 'ibge/bcim/unidades-federativas/PA/*',
'ibge/bcim/aldeias-indigenas/filter/geom/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/*or/geom/within/' + SERVER + 'ibge/bcim/unidades-federativas/PA/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/geom/*',
'ibge/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/geom/*or/' + SERVER + 'ibge/bcim/unidades-federativas/PR/*',
'ibge/bcim/municipios/within/{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}',
'ibge/bcim/municipios/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/*',
'ibge/bcim/municipios/filter/geom/overlaps/' + SERVER + 'ibge/bcim/unidades-federativas/ES/*or/geom/within/' + SERVER + 'ibge/bcim/unidades-federativas/ES/*and/geocodigo/startswith/32/',
'ibge/bcim/aldeias-indigenas/within/' + SERVER + 'ibge/bcim/unidades-federativas/PA/',
'ibge/bcim/aldeias-indigenas/within/' + SERVER + 'ibge/bcim/unidades-federativas/PA',
]

arr_get_for_spatial_operations = [
"ibge/bcim/unidades-federativas/ES/area",
"ibge/bcim/unidades-federativas/ES/boundary",
"ibge/bcim/unidades-federativas/ES/buffer/0.2",
"ibge/bcim/unidades-federativas/ES/centroid",
"ibge/bcim/unidades-federativas/ES/contains/" + SERVER + "ibge/bcim/aldeias-indigenas/587/",
"ibge/bcim/unidades-federativas/ES/convex_hull",
"ibge/bcim/aldeias-indigenas/587/coords",
"ibge/bcim/trechos-hidroviarios/59121/crosses/" + SERVER + "ibge/bcim/municipios/3126406",
"ibge/bcim/unidades-federativas/RJ/difference/" + SERVER + "ibge/bcim/municipios/3304300/",
"ibge/bcim/unidades-federativas/ES/dims",
"ibge/bcim/aldeias-indigenas/589/disjoint/" + SERVER + "ibge/bcim/unidades-federativas/RJ/",
"ibge/bcim/unidades-federativas/ES/distance/" + SERVER + "ibge/bcim/unidades-federativas/AM/",
"ibge/bcim/unidades-federativas/ES/empty",
"ibge/bcim/unidades-federativas/ES/envelope",
"ibge/bcim/unidades-federativas/ES/equals/" + SERVER + "ibge/bcim/unidades-federativas/ES/",
"ibge/bcim/unidades-federativas/ES/equals_exact/" + SERVER + "ibge/bcim/unidades-federativas/ES/",
"ibge/bcim/unidades-federativas/ES/ewkb",
"ibge/bcim/unidades-federativas/ES/ewkt",
"ibge/bcim/unidades-federativas/ES/extent",
"ibge/bcim/unidades-federativas/ES/geom_type",
"ibge/bcim/unidades-federativas/ES/geom_typeid",
"ibge/bcim/unidades-federativas/ES/hasz",
"ibge/bcim/unidades-federativas/ES/hex",
"ibge/bcim/unidades-federativas/ES/hexewkb",
"ibge/bcim/unidades-federativas/ES/intersection/" + SERVER + "ibge/bcim/unidades-federativas/RJ",
"ibge/bcim/unidades-federativas/ES/intersects/" + SERVER + "ibge/bcim/unidades-federativas/RJ/",
"ibge/bcim/aldeias-indigenas/587/json",
"ibge/bcim/aldeias-indigenas/587/kml",
"ibge/bcim/trechos-hidroviarios/59121/length",
"ibge/bcim/unidades-federativas/ES/num_geom",
"ibge/bcim/municipios/3301009/overlaps/" + SERVER + "ibge/bcim/unidades-federativas/ES",
"ibge/bcim/unidades-federativas/ES/point_on_surface",
"ibge/bcim/unidades-federativas/ES/relate/" + SERVER + "ibge/bcim/unidades-federativas/GO/",
"ibge/bcim/unidades-federativas/ES/relate_pattern/" + SERVER + "ibge/bcim/unidades-federativas/GO/*&FF*FF****",
"ibge/bcim/trechos-hidroviarios/59121/ring",
"ibge/bcim/unidades-federativas/ES/simple",
"ibge/bcim/unidades-federativas/ES/simplify/0.0&False",
"ibge/bcim/unidades-federativas/ES/srid",
"ibge/bcim/unidades-federativas/ES/srs",
"ibge/bcim/vegetacoes-de-restinga/2947/sym_difference/" + SERVER + "ibge/bcim/unidades-federativas/ES",
"ibge/bcim/unidades-federativas/AM/touches/" + SERVER + "ibge/bcim/unidades-federativas/RJ/",
"ibge/bcim/unidades-federativas/ES/transform/4326&false",
"ibge/bcim/unidades-federativas/ES/union/" + SERVER + "ibge/bcim/unidades-federativas/RJ",
"ibge/bcim/unidades-federativas/ES/valid",
"ibge/bcim/unidades-federativas/ES/valid_reason",
"ibge/bcim/aldeias-indigenas/587/within/" + SERVER + "ibge/bcim/unidades-federativas/ES/",
"ibge/bcim/unidades-federativas/ES/wkb",
"ibge/bcim/unidades-federativas/ES/wkt",
"ibge/bcim/aldeias-indigenas/589/x",
"ibge/bcim/aldeias-indigenas/589/y",
"ibge/bcim/aldeias-indigenas/589/z",
"ibge/bcim/trechos-hidroviarios/59121/x",
"ibge/bcim/trechos-hidroviarios/59121/y",
"ibge/bcim/trechos-hidroviarios/59121/z",
]

def test_requests(url_list):
    print("\n\n**********\nInitializing test set\n**********\n\n")

    requests_with_error = []
    for req_str in url_list:

        print('Executing: ' + SERVER + req_str)
        res = requests.get(SERVER + req_str)
        if res.status_code not in (200, 201,202,203,204,300,301,302,303):
            print('Failed: ' + SERVER + req_str + ' ' + str(res.status_code))
            requests_with_error.append(req_str)
    if len(requests_with_error) > 0:
        print("***************The urls below failed****************")
        for req_str_error in requests_with_error:
            print(SERVER + req_str_error)
        print("***************failed urls****************")
    else:
        print("*********Sucess***********")

    print("\n\n**********\nEnd of test set\n**********\n\n")

test_requests(arr_get_for_collection)
test_requests(arr_get_for_spatial_operations)






