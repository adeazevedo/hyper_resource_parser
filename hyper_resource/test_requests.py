import requests
from time import sleep
#se'rvidor = ''
#servidor = 'http://LUC00557347.ibge.gov.br/'
SERVER = 'http://LUC00557196:8000/'
#SERVER = "http://172.30.11.72:8000/"

arr_get_for_non_spatial_resource = [
    ("controle-list/usuario-list/1/", 200),
    ("controle-list/usuario-list/1/nome,email", 200),
]

arr_get_for_collection = [
    ('controle-list/gasto-list/count_resource', 200),
    ('controle-list/gasto-list/offset_limit/1&10', 200),
    ('controle-list/gasto-list/offset_limit/1&10/data,valor', 200),
    ('controle-list/gasto-list/group_by_count/tipo_gasto', 200),
    ('controle-list/gasto-list/filter/tipo_gasto/eq/3', 200),
    ('api/bcim/unidades-federativas/filter/geom/within/' + SERVER + 'api/bcim/municipios/3159407/geom/*', 200),
    ('api/bcim/unidades-federativas/?*contains=POINT(-42 -21)', 200),
    ('api/bcim/unidades-federativas/?*contains=POINT(-42 -21)&sigla=RJ', 200),
    ('api/bcim/unidades-federativas/?*contains=URL&sigla=RJ', 200),
    ('api/bcim/unidades-federativas/contains/POINT(-42 -21)', 200),
    ('api/bcim/aldeias-indigenas/within/POLYGON((-41.8 -21.2,-41.8 -17.8,-28.8 -17.8,-28.8 -21.,-41.8 -21.2))/', 200),
    ('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*', 200),
    ('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/PA/*', 200),
    ('api/bcim/unidades-federativas/filter/sigla/in/ES&PA/', 200),
    ('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*or/within/' + SERVER + 'api/bcim/unidades-federativas/PA/*', 200),
    ('api/bcim/aldeias-indigenas/filter/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/PA/*', 200),
    ('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    ('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    ('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*and/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    ('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    ('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*', 200),
    ('api/bcim/aldeias-indigenas/filter/id_objeto/eq/841/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/geom/*or/' + SERVER + 'api/bcim/unidades-federativas/PR/*', 200),
    ('api/bcim/municipios/within/{"type":"Polygon","coordinates":[[[-48.759514611370854,-28.3426735036349],[-48.631647133384185,-28.3426735036349],[-48.631647133384185,-28.082673631081306],[-48.759514611370854,-28.082673631081306],[-48.759514611370854,-28.3426735036349]]]}', 200),
    ('api/bcim/municipios/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*', 200),
    ('api/bcim/municipios/filter/geom/overlaps/' + SERVER + 'api/bcim/unidades-federativas/ES/*or/geom/within/' + SERVER + 'api/bcim/unidades-federativas/ES/*and/geocodigo/startswith/32/', 200),
    ('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/PA/', 200),
    ('api/bcim/aldeias-indigenas/within/' + SERVER + 'api/bcim/unidades-federativas/PA', 200),
    ('api/bcim/aldeias-indigenas/collect/nome&geom/buffer/0.5', 200),
    ('api/bcim/unidades-federativas/filter/sigla/in/RJ&ES/*collect/nome&geom/buffer/0.2', 200),
    ('api/bcim/aldeias-indigenas/offset_limit/0&2/nome,geom,nomeabrev/*collect/nome&geom/buffer/0.5', 400),
    ('api/bcim/aldeias-indigenas/offset_limit/0&2/nome,geom/*collect/geom/buffer/0.5', 400),
    ('api/bcim/unidades-federativas/filter/sigla/in/ES&PA/*projection/sigla,geocodigo', 200),
]

arr_get_for_spatial_operations = [
    ("api/bcim/unidades-federativas/ES/area", 200),
    ("api/bcim/unidades-federativas/ES/boundary", 200),
    ("api/bcim/unidades-federativas/ES/buffer/0.2", 200),
    ("api/bcim/unidades-federativas/ES/centroid", 200),
    ("api/bcim/unidades-federativas/ES/contains/" + SERVER + "api/bcim/aldeias-indigenas/587/", 200),
    ("api/bcim/unidades-federativas/ES/convex_hull", 200),
    ("api/bcim/aldeias-indigenas/587/coords", 200),
    ("api/bcim/trechos-hidroviarios/59121/crosses/" + SERVER + "api/bcim/municipios/3126406", 200),
    ("api/bcim/unidades-federativas/RJ/difference/" + SERVER + "api/bcim/municipios/3304300/", 200),
    ("api/bcim/unidades-federativas/ES/dims", 200),
    ("api/bcim/aldeias-indigenas/589/disjoint/" + SERVER + "api/bcim/unidades-federativas/RJ/", 200),
    ("api/bcim/unidades-federativas/ES/distance/" + SERVER + "api/bcim/unidades-federativas/AM/", 200),
    ("api/bcim/unidades-federativas/ES/empty", 200),
    ("api/bcim/unidades-federativas/ES/envelope", 200),
    ("api/bcim/unidades-federativas/ES/equals/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    ("api/bcim/unidades-federativas/ES/equals_exact/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    ("api/bcim/unidades-federativas/ES/ewkb", 200),
    ("api/bcim/unidades-federativas/ES/ewkt", 200),
    ("api/bcim/unidades-federativas/ES/extent", 200),
    ("api/bcim/unidades-federativas/ES/geom_type", 200),
    ("api/bcim/unidades-federativas/ES/geom_typeid", 200),
    ("api/bcim/unidades-federativas/ES/hasz", 200),
    ("api/bcim/unidades-federativas/ES/hex", 200),
    ("api/bcim/unidades-federativas/ES/hexewkb", 200),
    ("api/bcim/unidades-federativas/ES/intersection/" + SERVER + "api/bcim/unidades-federativas/RJ", 200),
    ("api/bcim/unidades-federativas/ES/intersects/" + SERVER + "api/bcim/unidades-federativas/RJ/", 200),
    ("api/bcim/aldeias-indigenas/587/json", 200),
    ("api/bcim/aldeias-indigenas/587/kml", 200),
    ("api/bcim/trechos-hidroviarios/59121/length", 200),
    ("api/bcim/unidades-federativas/ES/num_geom", 200),
    ("api/bcim/municipios/3301009/overlaps/" + SERVER + "api/bcim/unidades-federativas/ES", 200),
    ("api/bcim/unidades-federativas/ES/point_on_surface", 200),
    ("api/bcim/unidades-federativas/ES/relate/" + SERVER + "api/bcim/unidades-federativas/GO/", 200),
    ("api/bcim/unidades-federativas/ES/relate_pattern/" + SERVER + "api/bcim/unidades-federativas/GO/*&FF*FF****", 200),
    ("api/bcim/trechos-hidroviarios/59121/ring", 200),
    ("api/bcim/unidades-federativas/ES/simple", 200),
    ("api/bcim/unidades-federativas/ES/simplify/0.0&False", 200),
    ("api/bcim/unidades-federativas/ES/srid", 200),
    ("api/bcim/unidades-federativas/ES/srs", 200),
    ("api/bcim/vegetacoes-de-restinga/2947/sym_difference/" + SERVER + "api/bcim/unidades-federativas/ES", 200),
    ("api/bcim/unidades-federativas/AM/touches/" + SERVER + "api/bcim/unidades-federativas/RJ/", 200),
    ("api/bcim/unidades-federativas/ES/transform/4326&false", 200),
    ("api/bcim/unidades-federativas/ES/union/" + SERVER + "api/bcim/unidades-federativas/RJ", 200),
    ("api/bcim/unidades-federativas/ES/valid", 200),
    ("api/bcim/unidades-federativas/ES/valid_reason", 200),
    ("api/bcim/aldeias-indigenas/587/within/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    ("api/bcim/unidades-federativas/ES/wkb", 200),
    ("api/bcim/unidades-federativas/ES/wkt", 200),
    ("api/bcim/aldeias-indigenas/589/x", 200),
    ("api/bcim/aldeias-indigenas/589/y", 200),
    ("api/bcim/aldeias-indigenas/589/z", 200),
    ("api/bcim/trechos-hidroviarios/59121/x", 200),
    ("api/bcim/trechos-hidroviarios/59121/y", 200),
    ("api/bcim/trechos-hidroviarios/59121/z", 200),
]

arr_get_for_projection = [
    # only attributes
    ("api/bcim/unidades-federativas/nome", 200),
    ("api/bcim/unidades-federativas/nome/", 200),
    ("api/bcim/unidades-federativas/nome,geom", 200),
    ("api/bcim/unidades-federativas/nome,geom/", 200),
    ("api/bcim/unidades-federativas/projection/nome,geocodigo", 200), # attributes and projection
    ("api/bcim/unidades-federativas/projection/nome,geocodigo/", 200),
    # filter
    ("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES", 200),
    ("api/bcim/unidades-federativas/projection/nome,geocodigo/filter/sigla/in/RJ&ES", 200),
    # collect
    ("api/bcim/unidades-federativas/collect/geom&nome/upper", 200),
    ("api/bcim/unidades-federativas/projection/geom,nome/collect/geom&nome/upper", 200),
    ("api/bcim/unidades-federativas/projection/sigla,geocodigo/collect/geom&nome/upper", 400), # collected attributes not in projection (must fail)
    ("api/bcim/unidades-federativas/projection/sigla,geocodigo/collect/geom&sigla/lower", 400), # operated attribute in projection but lists differs (priorize projection in this case)
    # count_resource
    ("api/bcim/unidades-federativas/count_resource", 200),
    ("api/bcim/unidades-federativas/projection/nome,geocodigo/count_resource", 200),
    # filter_and_collect
    ("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES/*collect/geocodigo&sigla/lower", 200),
    ("api/bcim/unidades-federativas/projection/geocodigo,sigla/filter/sigla/in/RJ&ES/*collect/geocodigo&sigla/lower", 200),
    ("api/bcim/unidades-federativas/projection/geocodigo,sigla/filter/sigla/in/RJ&ES/*collect/sigla&geom/buffer/0.2", 400), # (must return status code 400)
    # filter_and_count_resource
    ("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES/*count_resource", 200),
    ("api/bcim/unidades-federativas/projection/nome,geocodigo/filter/sigla/in/RJ&ES/*count_resource", 200),
    # offset_limit
    ("api/bcim/unidades-federativas/offset_limit/0&2/", 200),
    ("api/bcim/unidades-federativas/offset_limit/0&2/nome,geocodigo/", 200),
    ("api/bcim/unidades-federativas/projection/geocodigo,sigla/offset_limit/0&2/", 200),
    ("api/bcim/unidades-federativas/projection/geocodigo,sigla/offset_limit/0&2/sigla,geocodigo/", 200),
    ("api/bcim/unidades-federativas/projection/geocodigo,sigla/offset_limit/0&2/nome,geocodigo,sigla/", 400),
    # distinct
    ("controle-list/usuario-list/distinct/email", 200),
    ("controle-list/usuario-list/distinct/id&nome&email", 200),
    ("controle-list/usuario-list/projection/nome,email,data_nascimento/distinct/nome&email", 200),
    # offset_limit_and_collect
    ("api/bcim/unidades-federativas/offset_limit/5&2/*collect/sigla&geom/buffer/0.8", 200),
    ("api/bcim/unidades-federativas/offset_limit/5&2/geom,sigla/*collect/sigla&geom/buffer/0.8", 200),
    ("api/bcim/unidades-federativas/offset_limit/5&2/sigla,geom,nome/*collect/sigla&geom/buffer/0.8", 400), # (must fail)
    ("api/bcim/unidades-federativas/projection/sigla,geom/offset_limit/5&2/*collect/sigla&geom/buffer/0.8", 200),
    ("api/bcim/unidades-federativas/projection/sigla,geom/offset_limit/5&2/sigla,geocodigo/*collect/sigla&geom/buffer/0.8", 400), # projection list == collect list != offset_limit list
    ("api/bcim/unidades-federativas/projection/sigla,geom/offset_limit/5&2/sigla,geom/*collect/nome&sigla&geom/buffer/0.8", 400), # projection list == offset_limit list != collect list
    ("api/bcim/unidades-federativas/projection/sigla,geom/offset_limit/5&2/sigla,geom/*collect/sigla&geom/buffer/0.8", 200), # projection list == offset_limit list == collect list

    #FeatureCollection operations
    ("api/bcim/aldeias-indigenas/within/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    ("api/bcim/aldeias-indigenas/projection/nome,nomeabrev/within/" + SERVER + "api/bcim/unidades-federativas/ES/", 200),
    ("api/bcim/unidades-federativas/contains/" + SERVER + "api/bcim/aldeias-indigenas/623", 200),
    ("api/bcim/unidades-federativas/projection/sigla,geom/contains/" + SERVER + "api/bcim/aldeias-indigenas/623", 200),
]

arr_get_for_complex_requests = [
    #("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/ES/*collect/geom/buffer/0.2/!union/(" + SERVER + "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/geom/buffer/0.2), 200),"
    ("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/ES/*collect/geom/buffer/0.2/!union!/" + SERVER + "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/geom/buffer/0.2", 200),
    ("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/ES/*collect/nome&geom/buffer/0.2/!union!/" + SERVER + "api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/nome&geom/buffer/0.2", 200),
    ("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/nome&geom/buffer/0.2/!union!/" + SERVER + "api/bcim/unidades-federativas/MG/envelope/", 200),
    ("api/bcim/aldeias-indigenas/filter/geom/within/" + SERVER + "api/bcim/unidades-federativas/AM/*collect/nome&geom/buffer/0.2/!union!/Polygon((-51.04196101779323 -22.915330279829785, -39.86109832699603 -22.915330279829785, -39.86109832699603 -14.227537498798952, -51.04196101779323 -14.227537498798952, -51.04196101779323 -22.915330279829785))", 200),
]

arr_get_for_geometry_collection_operation = [
    ("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/", 200),
    ("api/bcim/aldeias-indigenas/projection/nome/within/"+ SERVER +"api/bcim/unidades-federativas/ES/", 200),
    ("api/bcim/aldeias-indigenas/projection/geom,nome/within/"+ SERVER +"api/bcim/unidades-federativas/ES/", 200),
    ("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*count_resource", 200),
    ("api/bcim/aldeias-indigenas/projection/nome/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*count_resource", 200),
    ("api/bcim/aldeias-indigenas/projection/nome,geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*count_resource", 200),
    ("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome/upper", 200),
    ("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom&nome/upper", 200),
    ("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom/buffer/1.2", 200),
    ("api/bcim/aldeias-indigenas/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome&geom/buffer/1.2", 200),
    ("api/bcim/aldeias-indigenas/projection/nome/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome/upper", 200),
    ("api/bcim/aldeias-indigenas/projection/geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom/buffer/1.2", 200),
    ("api/bcim/aldeias-indigenas/projection/geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome&geom/buffer/1.2", 400),
    ("api/bcim/aldeias-indigenas/projection/nome,geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom&nome/upper", 200),
    ("api/bcim/aldeias-indigenas/projection/nome,geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/nome/upper", 400),
    ("api/bcim/aldeias-indigenas/projection/geom/within/"+ SERVER +"api/bcim/unidades-federativas/ES/*collect/geom&nome/upper", 400),
]

arr_get_for_spatialize_operation = [
        # FeatureResource (1 resource) join NonSpatialResource (1 resource)
    ("api/bcim/municipios/3304557/spatialize/geocodigo&geocodigo/http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/", 200),
    ('api/bcim/unidades-federativas/ES/spatialize/geocodigo&uf_geocodigo/{"uf_geocodigo":"32","pib_estimado":1000000000}', 200),
    #("api/bcim/unidades-federativas/ES/spatialize/geocodigo&geocodigo/http://gabriel:8880/estados-list/unidade-federativa-list/2/", 200),
        # FeatureResource (1 resource) join CollectionResource (n resources)
    ("api/bcim/municipios/3304557/spatialize/geocodigo&cod_municipio/http://172.30.10.86/api/pib-municipio/faturamento-list/filter/cod_municipio/eq/3304557", 200),
    #("api/bcim/unidades-federativas/ES/spatialize/geocodigo&geocodigo/http://gabriel:8880/estados-list/unidade-federativa-list/", 200),
        # FeatureResource join NonSpatialResource (Not joinable)
    ("api/bcim/municipios/3304557/spatialize/geocodigo&nome/http://172.30.10.86/api/munic-2015/planejamento-urbano-list/3243/", 400),
    #("api/bcim/unidades-federativas/ES/spatialize/geocodigo&nome/http://gabriel:8880/estados-list/unidade-federativa-list/2/", 400),
        # FeatureCollection (n resources) join CollectionResource (n resources)
    ("api/bcim/unidades-federativas/spatialize/geocodigo&cod_estado/http://172.30.10.86/esporte-list/cond-funcionamento-list/", 200),
    #("api/bcim/unidades-federativas/spatialize/geocodigo&geocodigo/http://gabriel:8880/estados-list/unidade-federativa-list/", 200),
        # CollectionResource (n resources) join FeatureCollection (n resources)
    #("esporte-list/cond-funcionamento-list/spatialize/cod_estado&geocodigo/http://172.30.10.86/api/bcim/unidades-federativas/offset_limit/0&2/geocodigo,nome,geom", 200),
    # FeatureCollection (n resources) join CollectionResource (n resources) - complex request
    ("api/bcim/unidades-federativas/filter/sigla/in/RJ&ES&MG/spatialize/geocodigo&cod_municipio/http://172.30.10.86/esporte-list/cond-funcionamento-list/filter/cod_estado/in/31&32&33&35/", 200),
]

def test_requests(url_status_code_tuple_list, test_label=''):
    default_init_test_label = "Initializing test set:"
    init_label_len = len(test_label) + len(default_init_test_label) + 5
    print("\n\n" + init_label_len * "*" + "\n* " + default_init_test_label  + " " + test_label + " *\n" + init_label_len * "*" + "\n\n")

    requests_with_error = []
    for url_status_code in url_status_code_tuple_list:

        print('Executing: ' + SERVER + url_status_code[0])
        res = requests.get(SERVER + url_status_code[0])
        if res.status_code != url_status_code[1]:#not in (200, 201,202,203,204,300,301,302,303):
            print('Failed: ' + SERVER + url_status_code[0] + ' ' + str(res.status_code) + ' != ' + str(url_status_code[1]) + ' (Expected)')
            url_status_code_status_ret = list(url_status_code)
            url_status_code_status_ret.append(res.status_code)
            requests_with_error.append( tuple(url_status_code_status_ret) )
    if len(requests_with_error) > 0:
        print("***************The urls below failed****************")
        for req_str_error in requests_with_error:
            print(SERVER + req_str_error[0] + ' ' + str(req_str_error[2]) + ' != ' + str(req_str_error[1]) + ' (Expected)')
        print("***************failed urls****************")
    else:
        print("*********Sucess***********")

    default_fin_test_label = "End of test set:"
    fin_label_len = len(test_label) + len(default_fin_test_label) + 5
    print("\n\n" + fin_label_len * "*" + "\n* " + default_fin_test_label + " " + test_label + " *\n" + fin_label_len * "*" + "\n\n")

test_requests(arr_get_for_non_spatial_resource, test_label = "Tests for NonSpatialResource")
test_requests(arr_get_for_collection, test_label="Generic tests to collection operations")
test_requests(arr_get_for_spatial_operations, test_label="Tests for spatial operations")
test_requests(arr_get_for_complex_requests, test_label="Tests for complex requests")
test_requests(arr_get_for_projection, test_label="Tests for FeatureCollection with and without projection")
test_requests(arr_get_for_geometry_collection_operation, test_label="Tests for spatial collection operations")
test_requests(arr_get_for_spatialize_operation, test_label="Tests for spatialize operation")

print("\n\n" + 25 * "X" + "\nX End of all test sets  X\n" + 25 * "X" + "\n\n")