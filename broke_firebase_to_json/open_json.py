from datetime import datetime
import json

with open("jsontratado.json", 'r') as f:
    data = json.load(f)

key = 1

for acesso in data:
    if 'timeline' in acesso[str(key)].keys():
        if 'inicio' in acesso[str(key)]['timeline']['0'].keys():
            timestamp = datetime.fromtimestamp(int(str(acesso[str(key)]['timeline']['0']['inicio'])[0:10]))
            dtInicio = str(timestamp)
            print(dtInicio)
    if 'municipio'in acesso[str(key)].keys():
        if acesso[str(key)]['municipio'] is not None:
            print(str(acesso[str(key)]['municipio']))
    key = key + 1