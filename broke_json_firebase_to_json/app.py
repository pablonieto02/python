from threading import Thread
import pandas as pd
import json

with open('broken_original/bruto-2019-08-16.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', 999)

def change_char(string, pos, change):
    return string[:pos]+change+string[pos+1:]

def limpar_aspas(texto):
    while True:
        if texto.find('\"') == -1:
            break

        left = texto.find('"') + 1
        right = texto[left+1:].find('"') + left + 1
        remove = texto[left:right].find("'")
        if remove != -1:
            texto = change_char(texto,left+remove,'')
            texto = change_char(texto,left-1,"'")
            texto = change_char(texto,right-1,"'")
        else:
            texto = change_char(texto,left-1,'')
            texto = change_char(texto,right-1,'')
    return texto

def limpar_url(texto):
    while True:
        if texto.find('<a') == -1:
            break

        left = texto.find('<a') + 1
        right = texto[left+1:].find('</a>') + left + 1

        texto = texto[:left-1] + texto[right+4:]
    return texto

def limpar_aspas_simples(texto):
    array_remove = []
    for left in range(1, len(texto)):
        if texto[left] == ":":
            if texto[left:left+3] == ": '":
                for right in range(left+2, len(texto)):
                    if texto[right] == "'":
                        if texto[right:right+2] == "'," or texto[right:right+2] == "'}":
                            if left+2 != right:
                                if texto[left+3:right].find("'") != -1:
                                    array_remove.append(left+3 + texto[left+3:right].find("'"))
                            break
    for remove in array_remove:
        texto = change_char(texto, remove, '@')
    array_remove = None
    return texto

def gerar_arquivo(df, num_thread):
    count = 1
    max = len(df)
    arquivo = '['
    for row in df.iterrows():
        linha = str(row[1])
        linha = limpar_aspas(linha)
        linha = limpar_aspas_simples(linha)
        linha = limpar_url(linha)
        linha = linha.replace('\\','')
        linha = linha.replace('usuarios    {','{').replace('False', '\'False\'').replace('True', '\'True\'')
        linha = linha.replace('\'','"' )
        linha = linha.replace('Name: '+row[0]+', dtype: object', '').replace('dadosHistorico', str(count))
        linha = linha.replace('}', '}\n')
        count += 1
        if count >= max:
            arquivo += linha + ']'
            break
        else:
            arquivo += linha + ','
    file = open('json_tratado_t' + str(num_thread) + '.json', 'w')
    file.write(arquivo)
    file.close()

class Th(Thread):
    def __init__ (self, df, num_thread):
        Thread.__init__(self)
        self.num_thread = num_thread
        self.df = df

    def run(self):
        gerar_arquivo(self.df,self.num_thread)

#for thread_number in range (2):
thread = Th(df[0:50000], 1)
thread.start()
thread = Th(df[50001:100000], 2)
thread.start()
thread = Th(df[100001:150000], 3)
thread.start()
thread = Th(df[150001:20000], 4)
thread.start()
thread = Th(df[20001:25000], 5)
thread.start()
thread = Th(df[25000:25001], 6)
thread.start()