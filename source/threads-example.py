import threading
import time


def breakfast(k):
    print('Iniciando breakfast...')
    time.sleep(k)
    print('Finalizando breakfast...')


def lunch(k):
    print('Iniciando lunch...')
    time.sleep(k)
    print('Finalizando lunch...')


def dinning(k):
    print('Iniciando dinning...')
    time.sleep(k)
    print('Finalizando dinning...')


inicio = time.perf_counter()

a = threading.Thread(target=breakfast, args=(3,))
a.start()
b = threading.Thread(target=lunch, args=(4,))
b.start()
c = threading.Thread(target=dinning, args=(5,))
c.start()

print("Hilos activos ", threading.active_count())

a.join()
b.join()
c.join()

# Ejecucion secuencial
# breakfast()
# lunch()
# dinning()

fin = time.perf_counter()
lap = fin - inicio

print('Tiempo tomado para las 3 tareas \n', lap)

print("Hilos activos ", threading.active_count())
# print(threading.enumerate())
