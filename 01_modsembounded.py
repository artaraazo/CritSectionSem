#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 11:23:53 2022

@author: artutaraperegmail.com
"""
from multiprocessing import Process, BoundedSemaphore
from multiprocessing import current_process
from multiprocessing import Value, Array
N = 8 #Hay 8 procesos
def task(common, tid, semaphore):
    a = 0
    for i in range(100): #numero de veces que iteras 
        print(f'{tid}−{i}: Non−critical Section')
        a += 1
        print(f'{tid}−{i}: End of non−critical Section')
        try:
            semaphore.acquire() #Semaforo rojo
            print(f'{tid}−{i}: Critical section') #la sección crítica es lo que hace el programa que en este caso es aumentar contador
            v = common.value + 1
            print(f'{tid}−{i}: Inside critical section')
            common.value = v
            print(f'{tid}−{i}: End of critical section')
        finally:
            semaphore.release()
def main():
    lp = []
    common = Value('i', 0) #variables compartidas las paso por argumento
    semaphore = BoundedSemaphore(1)
    for tid in range(N):
        lp.append(Process(target=task, args=(common, tid, semaphore))) #creo una lista con los 8 procesos.
    print (f"Valor inicial del contador {common.value}")
    for p in lp: #En este punto empiezan a ejecutarse los 8 a la vez
        p.start() #Barra vertical que separa los procesos
    for p in lp:
        p.join()  #Esperar a que acaben todos
    print (f"Valor final del contador {common.value}")
    print ("fin")
if __name__ == "__main__":
   main()