import csv
import json

geo_codigo = None
municipios = {}
csvfile = open('c:\dados\dados.gov.br\municipios.csv', 'r')
dict = {}
reader_file = csv.DictReader(csvfile, delimiter=";")
for row in reader_file:
    dict['Municipios'] = row['Codigo']

csvfile = open('c:\dados\dados.gov.br\procons-municipais-parana-6.csv', 'r')
reader_original_file = csv.DictReader(csvfile, delimiter=";")
fieldnames = ("Nome","Cargo","Orgao","Endereco", "DDD", "Telefone1", "E-mail", "Site")
#writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#writer.writeheader()
jsons = []
for row in reader_original_file:
    dic = {}
    for fn in fieldnames:
        dic[fn] = row[fn]
        if fn == "Orgao":
          munic_name = row[fn].strip().replace('Procon Municipal de ', '')
          geo_codigo = dict[munic_name]
    dic['geocodigo']= geo_codigo
    jsons.append(dic)
print(jsons)
#writer.writerow({fn: for fn in fieldnames:})

"""
jsonfile = open('c:\dados\dados.gov.br\procons-municipais-parana-6.json', 'w')
csv_rows = []
reader = csv.DictReader(csvfile, delimiter=";")
title = reader.fieldnames
for row in reader:
    csv_rows.extend([{title[i]:row[title] for i in range(len(title))}])

jsonfile.write(json.dumps(csv_rows))
jsonfile.close()
jsonfile =

"""