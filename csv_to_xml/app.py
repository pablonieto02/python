import csv
import subprocess as sp
import zipfile
import io

csv_file = open('Encontradas_PGENet_Para_Arquivar_Peixoto.csv', encoding='utf-8')
csv_reader = csv.reader(csv_file, delimiter=';')

def criar_arquivo(cda, data, fluxo, tipo_situacao, cdsituacao):

    conteudo_arquivo = '<?xml version="1.0" encoding="iso-8859-1"?>\n'\
    + '<Message>\n'\
    + '<MessageId>\n'\
    + '<ServiceId>AlteracaoSituacaoCda</ServiceId>\n'\
    + '<Version>1.0</Version>\n'\
    + '<MsgDesc>Alteração de situação CDA</MsgDesc>\n'\
    + '<Code>' + str(cdsituacao) + '</Code>\n'\
    + '<FromAddress>SEFAZBA</FromAddress>\n'\
    + '<ToAddress>PGEBA</ToAddress>\n'\
    + '<Date>' + ajustar_data(data) + '</Date>\n'\
    + '</MessageId>\n'\
    + '<MessageBody>\n'\
    + '<AlteracaoSituacaoCda>\n'\
    + '<nuCda>'+ str(cda) + '</nuCda>\n'\
    + '<idFluxo>'+ str(fluxo) +'</idFluxo>\n'\
    + '<cdSituacao>'+ tipo_situacao +'</cdSituacao>\n'\
    + '<dtEvento>' + ajustar_data(data) + '</dtEvento>\n'\
    + '</AlteracaoSituacaoCda>\n'\
    + '</MessageBody>\n'\
    + '</Message>\n'
    return str.encode(conteudo_arquivo, 'utf-8')

def loading(linha):
    tmp = sp.call('cls', shell=True)
    print('Linha: ' + str(linha))

def ajustar_data(a):
    return str.replace(a,'-', '')[:8]

mf = io.BytesIO()

count = 1
with zipfile.ZipFile(mf, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
    for row in csv_reader:
        count = count + 1
        zf.writestr(str(row[4]) + '.SIT.xml', criar_arquivo(row[0], row[2], row[1], '03', row[4]))
        zf.writestr(str(row[3]) + '.SIT.xml', criar_arquivo(row[0], row[2], row[1], '04', row[3]))


        if count > 10:
            break

with open("teste.zip", "wb") as f: # use `wb` mode
    f.write(mf.getvalue())
