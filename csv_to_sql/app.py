import pandas as pd
import pyodbc

constring = ''

# Abre um conexão unica para todas as operações
conn = pyodbc.connect(constring)
cursor = conn.cursor()

def execConsultaValorUnico(query):
    cursor.execute(query)
    retorno = '-1'
    for row in cursor.fetchall():
        retorno = row[0]
        break
    return retorno

def execConsultaValorDuplo(query):
    cursor.execute(query)
    retorno1 = -1
    retorno2 = -1
    for row in cursor.fetchall():
        retorno1 = row[0]
        retorno2 = row[1]
        break
    return retorno1, retorno2

def execConsultaValorTriplo(query):
    cursor.execute(query)
    retorno1 = -1
    retorno2 = -1
    retorno3 = -1
    for row in cursor.fetchall():
        retorno1 = row[0]
        retorno2 = row[1]
        retorno3 = row[2]
        break
    return retorno1, retorno2, retorno3

def converterFloat(valor):
    return float(valor.replace('.', '').replace('R$', '').strip(' ').replace(',','.'))

def obterPagSimulado(numContrato, anoContrato, valorSaldo):
    query = 'SELECT VALORTOTALCONT FROM dbo.Contrato WHERE NMCONTRATO = \'' + str(numContrato).zfill(5)  + '\' AND ano = \'' + str(anoContrato) + '\';'
    valorPagSimulado = float(execConsultaValorUnico(query)) - float(valorSaldo)
    return valorPagSimulado

def obterContrato(numContrato, anoContrato):
    query = 'SELECT Id_Contrato, idResponsavel, idCredor FROM dbo.Contrato WHERE NMCONTRATO = \'' + str(numContrato).zfill(5)  + '\' AND ano = \'' + str(anoContrato) + '\';'
    return execConsultaValorTriplo(query)

def obterContratoGestora(idContrato):
    query = 'SELECT idContratoGestora, idGestora FROM dbo.ContratoGestora WHERE idContrato = ' + str(idContrato) + ';'
    return execConsultaValorDuplo(query)

def insertContratoProcesso(numContrato, anoContrato, valorSaldo, idContratoGestora, valorTotal):
    query = 'INSERT dbo.ContratoProcesso (IdContratoGestora,DT_ENTRADA,NUMPROC,VALPAGO,DATAPAGO,FATURA,InicioCompetencia,' \
    + 'FinalCompetencia,IdUA,AnoCompetencia,MesCompetencia) VALUES (' + str(idContratoGestora) + ', CAST(N\'2019-01-21T00:00:00\' AS SmallDateTime),' \
    + ' N\'9999' + str(numContrato).zfill(5) + str(anoContrato) + '\''\
    + ',' + str(valorTotal) + ',CAST(N\'2018-12-31T00:00:00\' AS SmallDateTime), N\'Fatura Carga Simulada - Processo de Pagamento\',' \
    + 'CAST(N\'2018-01-01T00:00:00\' AS SmallDateTime),CAST(N\'2018-12-31T00:00:00\' AS SmallDateTime),1,N\'2018\',N\'12\')'
    return query

def insertProcesso(numContrato, anoContrato, valorSaldo, idGestora, idResponsavel, idCredor):
    query = 'INSERT dbo.Processo (PROCPRODEB,MESCOMPETENCIA,ANOCOMPETENCIA,ATIVIDADE,idCredor,DTENTRADA,VALFATURA,idGestora,idResponsavel,'\
    + 'TIPODOCUMENTO,NUMEMP,NUMELEM,DTEMP,NUMEMP2,NUMELEM2,LTPROC,OBS,Localizacao,IdUA,'\
    + 'ProcCotaPatronal,DevolucaoCaucao) VALUES ( \'9999' + str(numContrato).zfill(5) + str(anoContrato) + '\''\
    + ', \'01\', \'2018\', \'01\',' + str(idCredor) + ',CAST(\'2019-01-21T00:00:00\' AS SmallDateTime),'\
    + str(valorTotal) +  ', ' + str(idGestora) + ', ' + str(idResponsavel) + ', \'Nota Fiscal\',\'999999\',\'999999\',CAST(\'2018-01-01T00:00:00\' AS SmallDateTime),'\
    + '\'\',\'\',\'N\',\'Carga Simulada Atualização Saldo - Processo\',\'\',1,\'\',\'N\');'
    return query

def updateContratoGestora(idContrato, valorTotal):
    query = 'UPDATE dbo.ContratoGestora SET PagoTotal = ' + str(valorTotal) + ' WHERE idContrato = ' + str(idContrato) + ';'
    return query

def updateTotalContrato(idContrato, valorTotal):
    query = 'UPDATE dbo.Contrato SET PagoTotal = ' + str(valorTotal) + ',  WHERE Id_Contrato = ' + str(idContrato) + ';'
    return query
#
# Inicio
#
df = pd.read_csv('CONPAG.csv', sep=';')
filesql = open('scripts.sql','w')
fileerros = open('erros.sql','w')
for i, row in df.iterrows():
    #if i >= 1:
    #    breaks
    numContrato = row['numero']
    anoContrato = row['ano']
    valorSaldo =  converterFloat(row['saldo'])

    valorTotal = round(obterPagSimulado(numContrato, anoContrato, valorSaldo), 2)
    idContrato, idResponsavel, idCredor = obterContrato(numContrato, anoContrato)
    idContratoGestora, idGestora = obterContratoGestora(idContrato)

    if idContrato != -1 and float(valorTotal) >= float(0):
        filesql.write(insertContratoProcesso(numContrato, anoContrato, valorSaldo, idContratoGestora, valorTotal))
        filesql.write('\n')
        filesql.write(updateContratoGestora(idContrato, valorTotal)) ################## AJUSTAR SALDO  saldo = VALORTOTALCONT - PAGOTOTAL
        filesql.write('\n')
        filesql.write(updateTotalContrato(idContrato, valorTotal))
        filesql.write('\n')
        filesql.write(insertProcesso(numContrato, anoContrato, valorSaldo, idGestora, idResponsavel, idCredor))
    else:
        fileerros.write('numContrato: ' + str(numContrato) + ', anoContrato: ' + str(anoContrato) + ', saldo: ' + str(valorTotal))
        fileerros.write('\n')
    # INSERT PROCESSO
    # UPDATE TOTAL EM CONTRATO GESTORA

# Fecha a conexão
cursor.close()
conn.close()
