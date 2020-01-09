import requests 

url = 'https://us-central1-oi-contabilizei.cloudfunctions.net/docs/criptografia/hash'

param = 'gustavo.castanho@gmail.com'
PARAMS = {'pass':param}

r = requests.get(url = url, params = PARAMS) 

print(r.text)