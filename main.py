import threading
import time
import numpy as np

ordem = []
ordemAux = []


def chegada():
    processos = fila.copy()
    temptotal = processos[1].sum() + min(fila[2])
    while temptotal > 0:
        #varro a parte do AT
        for i in range(len(processos[0])):
            # se o tempo de chegada for zero coloco na lista
            if processos[2][i] == 0:
                ordem.append(i)
                ordemAux.append(i)
            #se o tempo de chegada for maior que zero eu subitraio
            if processos[2][i] >= 0:
                processos[2][i] -= 1
        temptotal -= 1
        time.sleep(1/1000)


def fifo(TempTotal, tmff, TempIn):
    proff = fila.copy()
    TempAux = 0
    proant = -1
    while TempAux <= TempTotal:
        if min(proff[2]) <= TempAux:
            if (proant + 1) != proff[0][ordem[0]]:
                print("-" * 50)
                print(f"processo {ordem[0] + 1} está executando!")
                proant = ordem[0]
            #conferir se algum processo chegou
            print(f"Tempo de execução até o momento: {TempAux}ms")
            proff[1][ordem[0]] -= 1
            time.sleep(1/1000)
            TempAux += 1
            #se o tempo do processo acabou eu tiro ele da lista de execução
            #indico quando este processo entrou para execução
            if proff[1][ordem[0]] == 0:
                tmff[0][ordem[0]] = TempIn
                proant = ordem[0]
                TempIn = TempAux
                ordem.pop(0)
                if len(ordem) == 0:
                    print("-"*50)
                    print("Não há mais processos, Execucao finalizadas!")
                    print(f"Tempo de execução até o momento: {TempAux}")
                    print(f"Processos finalizados!")
                    print("*"*50)
                    print(f"Calculo do tempo medio FIFO")
                    calctemp(tmff)
                    print("*"*50)
                    break
        else:
            print("-" * 50)
            print(f"Aguardando processo para executar!")
            print(f"Tempo de execução até o momento: {TempAux}")
            time.sleep(1 / 1000)
            TempAux += 1


def rr(TempTotal, tmrr, TempIn, qt):
    prorr = fila.copy()
    TempAux = 0
    qtaux = 0
    proant = -1
    proantaux = ordemAux[0]
    while TempAux <= TempTotal:
        if min(prorr[2]) <= TempAux:
            if (proant+1) != prorr[0][ordemAux[0]]:
                tmrr[1][ordemAux[0]] = prorr[1][ordemAux[0]] - fila[1][ordemAux[0]]  # tempo que já executou
                print("-" * 50)
                print(f"processo {ordemAux[0] + 1} está executando!")
                proant = ordemAux[0]
            # conferir se algum processo chegou
            print(f"Tempo de execução até o momento: {TempAux}ms")
            prorr[1][ordemAux[0]] -= 1
            time.sleep(1 / 1000)
            TempAux += 1
            qtaux += 1

            # se o tempo do processo acabou eu tiro ele da lista de execução
            # indico quando este processo entrou para execução
            if prorr[1][ordemAux[0]] == 0:
                qtaux = 0
                if (proantaux + 1) != prorr[0][ordemAux[0]]:
                    tmrr[0][ordemAux[0]] = TempIn #Tempo que entrou pra executar
                proantaux = ordemAux[0]
                TempIn = TempAux
                ordemAux.pop(0)
                if len(ordemAux) == 0:
                    print("-" * 50)
                    print("Não há mais processos, Execucao finalizadas!")
                    print(f"Tempo de execução até o momento: {TempAux}")
                    print(f"Processos finalizados!")
                    print("*" * 50)
                    print(f"Calculo do tempo medio RR")
                    calctemp(tmrr)
                    print("*" * 50)
                    break

            elif qtaux == qt:
                qtaux = 0
                if (proantaux + 1) != prorr[0][ordemAux[0]]:
                    tmrr[0][ordemAux[0]] = TempIn #Tempo que entrou pra executar
                TempIn = TempAux
                proant = ordemAux[0]
                proantaux = ordemAux[0]
                ordemAux.append(ordemAux[0])
                ordemAux.pop(0)
        else:
            print("-" * 50)
            print(f"Aguardando processo para executar!")
            print(f"Tempo de execução até o momento: {TempAux}")
            time.sleep(1 / 1000)
            TempAux += 1


def calctemp(tm):
    print(f"Matriz para claculo do tempo medio "
          f"\nProcessos                    : {fila[0]}"
          f"\nTempo da ultima execucao     : {tm[0]}"
          f"\nTempo ja executado           : {tm[1]}"
          f"\nTempo que o processo apareceu: {tm[2]}")
    tmaux = tm.sum(axis=0)
    for i in range(len(tmaux)):
        print(f"O tempo de espera do processo {i+1} foi de: {tmaux[i]}ms")
    print(f"O tempo médio total foi de {round(tmaux.sum()/len(tmaux),2)}ms")


#Inicio
process = np.array([1,2,3,4,5])
bt =      np.array([10,1,2,1,5])
at =      np.array([0,0,0,0,0])
fila = np.concatenate((process, bt, at)).reshape(3, len(process))
tempomedio = np.concatenate((np.zeros(2*len(process)), -1*at)).reshape(3, len(process))
TempoTotal = bt.sum() + min(fila[2])
print("*"*50)
print(f"Iniciando a execução")
x = threading.Thread(target=chegada, args=())
y = threading.Thread(target=fifo, args=(TempoTotal, tempomedio, min(fila[2])))
z = threading.Thread(target=rr, args=(TempoTotal, tempomedio, min(fila[2]), 1))
x.start()
y.start()
z.start()
# chegada()
# fifo(TempoTotal, tempomedio,min(fila[2]))
# rr(TempoTotal, tempomedio,min(fila[2]), 1)
