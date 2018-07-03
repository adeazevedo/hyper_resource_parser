import requests
from time import sleep
#se'rvidor = ''
#servidor = 'http://LUC00557347.ibge.gov.br/'
SERVER = 'http://LUC00557196.ibge.gov.br:8000/'
#SERVER = "http://172.30.11.72:8000/"

arr_get_for_collection = [
    'controle-list/gasto-list/count_resource',
    'controle-list/gasto-list/offset_limit/1&10',
    'controle-list/gasto-list/offset_limit/1&10/data,valor',
    'controle-list/gasto-list/group_by_count/tipo_gasto',
    'controle-list/gasto-list/filter/tipo_gasto/eq/3',
    'api/bcim/unidades-federativas/filter/geom/within/' + SERVER + 'api/bcim/municipios/3159407/geom/*',
    'api/bcim/unidades-federativas/?*contains=POINT(-42 -21)',
    'api/bcim/unidades-federativas/?*contains=POINT(-42 -21)&sigla=RJ',
    'api/bcim/unidades-federativas/?*contains=URL&sigla=RJ',
    'api/bcim/unidades-federativas/contains/POINT(-42 -21)',
    'api/bcim/aldeias-indigenas/within/POLYGON((-41.8 -21.2,-41.8 -17.8,-28.8 -17.8,-28.8 -21.,-41.8 -21.2))/',
    'api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*',
    'api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/PA/*',
    'api/bcim/unidades-federativas/filter/sigla/in/ES&PA/',
    'api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*or/within/' + SERVER + 'api/bcim/unidades-federativas/PA/*',
    'api/bcim/aldeias-indigenas/filter/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/PA/*',
    'api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*',
    'api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*',
    'api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*',
    'api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*',
    'api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*',
    'api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*or/' + SERVER + 'api/bcim/unidades-federativas/PR/*',
    'api/bcim/municipios/within/{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}',
    'api/bcim/municipios/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*',
    'api/bcim/municipios/filter/geom/overlaps/' + SERVER + 'api/bcim/unidades-federativas/ES/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*and/geocodigo/startswith/32/',
    'api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/PA/',
    'api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/PA',
    'api/bcim/aldeias-indigenas/collect/nome&geom/buffer/0.5',
    'api/bcim/unidades-federativas/filter/sigla/in/RJ&ES/*collect/nome&geom/buffer/0.2',
    'api/bcim/aldeias-indigenas/offset_limit/0&2/nome,geom,nomeabrev/*collect/nome&geom/buffer/0.5',
    'api/bcim/aldeias-indigenas/offset_limit/0&2/nome,geom/*collect/geom/buffer/0.5',
    'api/bcim/unidades-federativas/filter/sigla/in/ES&PA/*projection/sigla,geocodigo'
]

arr_get_for_spatial_operations = [
    "api/bcim/unidades-federativas/ES/area",
    "api/bcim/unidades-federativas/ES/boundary",
    "api/bcim/unidades-federativas/ES/buffer/0.2",
    "api/bcim/unidades-federativas/ES/centroid",
    "api/bcim/unidades-federativas/ES/contains/" + SERVER + "api/bcim/aldeias-indigenas/587/",
    "api/bcim/unidades-federativas/ES/convex_hull",
    "api/bcim/aldeias-indigenas/587/coords",
    "api/bcim/trechos-hidroviarios/59121/crosses/" + SERVER + "api/bcim/municipios/3126406",
    "api/bcim/unidades-federativas/RJ/difference/" + SERVER + "api/bcim/municipios/3304300/",
    "api/bcim/unidades-federativas/ES/dims",
    "api/bcim/aldeias-indigenas/589/disjoint/" + SERVER + "api/bcim/unidades-federativas/RJ/",
    "api/bcim/unidades-federativas/ES/distance/" + SERVER + "api/bcim/unidades-federativas/AM/",
    "api/bcim/unidades-federativas/ES/empty",
    "api/bcim/unidades-federativas/ES/envelope",
    "api/bcim/unidades-federativas/ES/equals/" + SERVER + "api/bcim/unidades-federativas/ES/",
    "api/bcim/unidades-federativas/ES/equals_exact/" + SERVER + "api/bcim/unidades-federativas/ES/",
    "api/bcim/unidades-federativas/ES/ewkb",
    "api/bcim/unidades-federativas/ES/ewkt",
    "api/bcim/unidades-federativas/ES/extent",
    "api/bcim/unidades-federativas/ES/geom_type",
    "api/bcim/unidades-federativas/ES/geom_typeid",
    "api/bcim/unidades-federativas/ES/hasz",
    "api/bcim/unidades-federativas/ES/hex",
    "api/bcim/unidades-federativas/ES/hexewkb",
    "api/bcim/unidades-federativas/ES/intersection/" + SERVER + "api/bcim/unidades-federativas/RJ",
    "api/bcim/unidades-federativas/ES/intersects/" + SERVER + "api/bcim/unidades-federativas/RJ/",
    "api/bcim/aldeias-indigenas/587/json",
    "api/bcim/aldeias-indigenas/587/kml",
    "api/bcim/trechos-hidroviarios/59121/length",
    "api/bcim/unidades-federativas/ES/num_geom",
    "api/bcim/municipios/3301009/overlaps/" + SERVER + "api/bcim/unidades-federativas/ES",
    "api/bcim/unidades-federativas/ES/point_on_surface",
    "api/bcim/unidades-federativas/ES/relate/" + SERVER + "api/bcim/unidades-federativas/GO/",
    "api/bcim/unidades-federativas/ES/relate_pattern/" + SERVER + "api/bcim/unidades-federativas/GO/*&FF*FF****",
    "api/bcim/trechos-hidroviarios/59121/ring",
    "api/bcim/unidades-federativas/ES/simple",
    "api/bcim/unidades-federativas/ES/simplify/0.0&False",
    "api/bcim/unidades-federativas/ES/srid",
    "api/bcim/unidades-federativas/ES/srs",
    "api/bcim/vegetacoes-de-restinga/2947/sym_difference/" + SERVER + "api/bcim/unidades-federativas/ES",
    "api/bcim/unidades-federativas/AM/touches/" + SERVER + "api/bcim/unidades-federativas/RJ/",
    "api/bcim/unidades-federativas/ES/transform/4326&false",
    "api/bcim/unidades-federativas/ES/union/" + SERVER + "api/bcim/unidades-federativas/RJ",
    "api/bcim/unidades-federativas/ES/valid",
    "api/bcim/unidades-federativas/ES/valid_reason",
    "api/bcim/aldeias-indigenas/587/within/" + SERVER + "api/bcim/unidades-federativas/ES/",
    "api/bcim/unidades-federativas/ES/wkb",
    "api/bcim/unidades-federativas/ES/wkt",
    "api/bcim/aldeias-indigenas/589/x",
    "api/bcim/aldeias-indigenas/589/y",
    "api/bcim/aldeias-indigenas/589/z",
    "api/bcim/trechos-hidroviarios/59121/x",
    "api/bcim/trechos-hidroviarios/59121/y",
    "api/bcim/trechos-hidroviarios/59121/z",
]

arr_get_for_projection = [
    # only attributes
    "api/bcim/unidades-federativas/nome",
    "api/bcim/unidades-federativas/nome/",
    "api/bcim/unidades-federativas/nome,geom",
    "api/bcim/unidades-federativas/nome,geom/",
    "api/bcim/unidades-federativas/projection/nome,geocodigo", # attributes and projection
    "api/bcim/unidades-federativas/projection/nome,geocodigo/",
    # filter
    "api/bcim/unidades-federativas/filter/sigla/in/RJ&ES",
    "api/bcim/unidades-federativas/projection/nome,geocodigo/filter/sigla/in/RJ&ES",
    # collect
    "api/bcim/unidades-federativas/collect/geom&nome/upper",
    "api/bcim/unidades-federativas/projection/geom,nome/collect/geom&nome/upper",
    "api/bcim/unidades-federativas/projection/sigla,geocodigo/collect/geom&nome/upper", # collected attributes not in projection (must fail)
    "api/bcim/unidades-federativas/projection/sigla,geocodigo/collect/geom&sigla/lower", # operated attribute in projection but lists differs (priorize projection in this case)
    # count_resource
    "api/bcim/unidades-federativas/count_resource",
    "api/bcim/unidades-federativas/projection/nome,geocodigo/count_resource",
    # filter_and_collect
    "api/bcim/unidades-federativas/filter/sigla/in/RJ&ES/*collect/geocodigo&sigla/lower",
    "api/bcim/unidades-federativas/projection/geocodigo,sigla/filter/sigla/in/RJ&ES/*collect/geocodigo&sigla/lower",
    "api/bcim/unidades-federativas/projection/geocodigo,sigla/filter/sigla/in/RJ&ES/*collect/sigla&geom/buffer/0.2", # (must return status code 400)
    # filter_and_count_resource
    "api/bcim/unidades-federativas/filter/sigla/in/RJ&ES/*count_resource",
    "api/bcim/unidades-federativas/projection/nome,geocodigo/filter/sigla/in/RJ&ES/*count_resource",
    # offset_limit
    "api/bcim/unidades-federativas/offset_limit/0&2/",
    "api/bcim/unidades-federativas/offset_limit/0&2/nome,geocodigo/",
    "api/bcim/unidades-federativas/projection/geocodigo,sigla/offset_limit/0&2/",
    "api/bcim/unidades-federativas/projection/geocodigo,sigla/offset_limit/0&2/sigla,geocodigo/",
    "api/bcim/unidades-federativas/projection/geocodigo,sigla/offset_limit/0&2/nome,geocodigo,sigla/",
    # distinct
    "controle-list/usuario-list/distinct/email",
    "controle-list/usuario-list/distinct/id&nome&email",
    "controle-list/usuario-list/projection/nome,email,data_nascimento/distinct/nome&email",
    # offset_limit_and_collect
    "api/bcim/unidades-federativas/offset_limit/5&2/*collect/sigla&geom/buffer/0.8",
    "api/bcim/unidades-federativas/offset_limit/5&2/geom,sigla/*collect/sigla&geom/buffer/0.8",
    "api/bcim/unidades-federativas/offset_limit/5&2/sigla,geom,nome/*collect/sigla&geom/buffer/0.8",# (must fail)
    "api/bcim/unidades-federativas/projection/sigla,geom/offset_limit/5&2/*collect/sigla&geom/buffer/0.8",
    "api/bcim/unidades-federativas/projection/sigla,geom/offset_limit/5&2/sigla,geocodigo/*collect/sigla&geom/buffer/0.8", # projection list == collect list != offset_limit list
    "api/bcim/unidades-federativas/projection/sigla,geom/offset_limit/5&2/sigla,geom/*collect/nome&sigla&geom/buffer/0.8", # projection list == offset_limit list != collect list
    "api/bcim/unidades-federativas/projection/sigla,geom/offset_limit/5&2/sigla,geom/*collect/sigla&geom/buffer/0.8", # projection list == offset_limit list == collect list

    #FeatureCollection operations
    "api/bcim/aldeias-indigenas/within/" + SERVER + "api/bcim/unidades-federativas/ES/",
    "api/bcim/aldeias-indigenas/projection/nome,nomeabrev/within/" + SERVER + "api/bcim/unidades-federativas/ES/",
    "api/bcim/unidades-federativas/contains/" + SERVER + "api/bcim/aldeias-indigenas/623",
    "api/bcim/unidades-federativas/projection/sigla,geom/contains/" + SERVER + "api/bcim/aldeias-indigenas/623"
]

arr_get_for_complex_requests = [
    #"api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/ES/*collect/geom/buffer/0.2/!union/(" + SERVER + "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/geom/buffer/0.2)"
    "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/ES/*collect/geom/buffer/0.2/!union/" + SERVER + "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/geom/buffer/0.2",
    "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/ES/*collect/nome&geom/buffer/0.2/!union/" + SERVER + "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/nome&geom/buffer/0.2",
    "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/nome&geom/buffer/0.2/!union/" + SERVER + "api/bcim/unidades-federativas/MG/envelope/",
    "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/nome&geom/buffer/0.2/!union/Polygon((-51.04196101779323 -22.915330279829785, -39.86109832699603 -22.915330279829785, -39.86109832699603 -14.227537498798952, -51.04196101779323 -14.227537498798952, -51.04196101779323 -22.915330279829785))",
]

def test_requests(url_list):
    print("\n\n" + 20 * "*" + "\nInitializing test set\n" + 20 * "*" + "\n\n")

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

    print("\n" + 20 * "-" + "End of this test set" + 20 * "-" + "\n")

test_requests(arr_get_for_collection)
test_requests(arr_get_for_spatial_operations)
test_requests(arr_get_for_complex_requests)
test_requests(arr_get_for_projection)

print("\n\n" + 20 * "*" + "\nEnd of all test sets\n" + 20 * "*" + "\n\n")