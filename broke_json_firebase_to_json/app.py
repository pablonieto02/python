from threading import Thread
from multiprocessing import Process
import functions as fu
import pandas as pd
import json

print('lendo arquivo...')
with open('broken_original/bruto-2019-08-16.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', 999)

class Th(Thread):
    def __init__ (self, df, num_thread, caminho):
        Thread.__init__(self)
        self.num_thread = num_thread
        self.df = df
        self.caminho = caminho
    def run(self):        
        fu.gerar_arquivo(self.df,self.num_thread, self.caminho)

# Start App
print('start App...')
caminho = 'json_temp/json_thread'
len_df = len(df)
print ('lean: ' + str(len_df))
index = 0
index_range = 40000
thread_number = 0
procs = []

if __name__ == '__main__':
    while True:
        thread_number += 1
        print('processor ' + str(thread_number) + ' iniciado')
        if index + index_range < len_df:
            end = index + index_range
            print('index de: ' + str(index) + ' até: ' + str(end))
            proc = Process(target=fu.gerar_arquivo, args=(df[index:end], thread_number, caminho,))
            procs.append(proc)
            proc.start()
        else:
            end = len_df
            print('index de: ' + str(index) + ' até: ' + str(end))
            proc = Process(target=fu.gerar_arquivo, args=(df[index:end], thread_number, caminho,))
            procs.append(proc)
            proc.start()
            break
        index += index_range

    for proc in procs:
        proc.join()