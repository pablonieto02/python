import requests
import csv
import time
import hashlib

url = 'https://us-central1-oi-contabilizei.cloudfunctions.net/docs/criptografia/hash'

csv_file = open('novembro.csv')
export_file = open('novembro_export_p2.csv','w')

csv_reader = csv.reader(csv_file, delimiter=',')

line_count = 0
for row in csv_reader:
    line_count = line_count + 1
    if line_count >= 2469:
        print(line_count)
        param = row[0]
        PARAMS = {'pass':param}
        retorno = requests.get(url = url, params = PARAMS) 
        export_file.write(param + ',' + retorno.text)
        export_file.write('\n')
        time.sleep(0.3)