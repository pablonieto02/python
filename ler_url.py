import requests
import csv 

url = 'https://us-central1-oi-contabilizei.cloudfunctions.net/docs/criptografia/hash'

export_file = open('user_key_pre_cadastro_no_aprovado.csv','w')
csv_file = open('pre_cadastro_no_aprovado.csv')

csv_reader = csv.reader(csv_file, delimiter=',')

line_count = 0
for row in csv_reader:
    line_count = line_count + 1
    print(line_count)
    param = row[0]
    PARAMS = {'pass':param}
    retorno = requests.get(url = url, params = PARAMS) 
    export_file.write(param + ',' + retorno.text)
    export_file.write('\n')