from multiprocessing import Process, Manager
import time

def gerar_arquivo(l, gp):
    print('processado: ' + str(gp))
    time.sleep(30)
    l[gp] = True

def get_proc(list_procs):
    for k,v in list_procs.items():
        if v:
            list_procs[k] = False
            return k
    return -1

# Start App
print('start App...')

thread_number = 0
procs = []

if __name__ == '__main__':
    manager = Manager()
    list_procs = manager.dict({ 1: True, 2: True, 3: True, 4: True, 5: True, 6: True })
    
    while True:
        gp = get_proc(list_procs)
        if gp != -1:
            thread_number += 1
            proc = Process(target=gerar_arquivo, args=(list_procs,gp,))
            procs.append(proc)
            proc.start()
        else:
            print('esperando...')
            time.sleep(10)
            print(thread_number)
        if thread_number > 13:
            break

    for proc in procs:
        proc.join()