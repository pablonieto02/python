from multiprocessing import Process, Manager
import functions as fu
import pandas as pd
import json
import time

print('lendo arquivo...')
with open('', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
del df['qualificacao']
df = df.dropna()

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', 999)

def gerar_arquivo(df, num_thread, caminho, list_procs, pkey, index, end):
    print('iniciado - de: ' + str(index) + ', até: ' + str(end) + ', arquivo: ' + str(thread_number) + ', thread: ' + str(pkey))
    fu.gerar_arquivo(df, num_thread, caminho)
    list_procs[pkey] = True
    print('finalizado - de: ' + str(index) + ', até: ' + str(end) + ', arquivo: ' + str(thread_number) + ' thread: ' + str(pkey))

def get_proc(list_procs):
    for k,v in list_procs.items():
        if v:
            list_procs[k] = False
            return k
    return -1

# Start App
print('start App...')
caminho = 'json_temp/json_thread'
len_df = len(df)
print ('len: ' + str(len_df))
index = 0
index_range = 30000
thread_number = 0
procs = []
z = 0

if __name__ == '__main__':
    manager = Manager()
    list_procs = manager.dict({ 1: True, 2: True, 3: True, 4: True, 5: True, 6: True})
    
    while True:
        pkey = get_proc(list_procs)
        if pkey != -1:
            thread_number += 1
            if thread_number > 1:
                z = 1
            if index + index_range < len_df:
                end = index + index_range
                proc = Process(target=gerar_arquivo, args=(df[index+z:end],thread_number,caminho,list_procs,pkey,index+z,end,))
                procs.append(proc)
                proc.start()
            else:
                end = len_df
                proc = Process(target=gerar_arquivo, args=(df[index+z:end],thread_number,caminho,list_procs,pkey,index+z,end,))
                procs.append(proc)
                proc.start()
                break
            index += index_range
        else:
            print('esperando...')
            time.sleep(15)
    for proc in procs:
        proc.join()
