import os
import json

path = '/home/pablo/github/python/broke_firebase_to_json/json_temp'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(os.path.join(r, file))

for f in files:
    try:
        with open(f, 'r') as f:
            data = json.load(f)
            print(str(f) + ' OK!')
    except Exception as e:
        print(str(f) + ' ERRO!')
        print('Failed to upload to ftp: '+ str(e))