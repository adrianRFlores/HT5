import simpy
import random
import math

procesos = int(input("Ingrese la cantidad de procesos: "))
intervalo = int(input("Ingrese el intervalo de entrada de procesos: "))
tiempos = [] #Array para almacenar los tiempos finales de cada proceso
random.seed(10)

def std(data):
    n = len(data)
    # Media
    mean = sum(data) / n
    # Desviaciones
    deviations = [(x - mean) ** 2 for x in data]
    # Varianza
    variance = sum(deviations) / n
    #Desviacion estandar
    return math.sqrt(variance) 

#Generador de procesos
def genProceso(env, name, ram, cpu):
    global totalT
    
    expo = int(random.expovariate(1.0/intervalo))
    yield env.timeout(expo) #Espera una cantidad de tiempo segun el intervalo alimentado a la funcion expovariate
    
    instrucciones = random.randint(1, 10) #Genera las instrucciones del proceso
    mem = random.randint(1,10) #Genera la cantidad de memoria que utiliza el proceso
    tEntrada = env.now #Toma el tiempo al que entra el proceso a la computadora
    
    with ram.get(mem) as entrada:
        yield entrada #Entra en la cola para la RAM
        
        estado = 2
        while(instrucciones > 0):
            
            #Si tiene un estado = 1, entra en la cola de waiting por un ciclo
            if(estado == 1):
                with io.request() as waiting:
                    yield waiting
                    env.timeout(1)
                estado = 2    
            
            #Si es ready y tiene instrucciones pendientes, entra a la cola del CPU
            while((estado == 2) and (instrucciones > 0)):
                with cpu.request() as activo:
                    yield activo
                    yield env.timeout(1)
                    instrucciones -= 3
                estado = random.randint(1,2) #Genera un estado aleatorio (1 = waiting, 2 = ready)
        
        yield ram.put(mem) #Devuelve la memoria a la RAM
       
    tfinal = env.now - tEntrada #Toma el tiempo final
    print(name + ": %d" %tfinal)
    tiempos.append(tfinal)
    totalT += tfinal

env = simpy.Environment() 
ram = simpy.Container(env, init = 100, capacity = 100)
cpu = simpy.Resource(env, capacity = 1)
io = simpy.Resource(env)

totalT = 0
#Se generan los procesos a mandar a la RAM
for i in range(procesos):
    env.process(genProceso(env, "proceso %d"%i, ram, cpu))

env.run()

print("\nTiempo total: %f" %totalT)
print("Tiempo promedio: %f" %(totalT/procesos))
print("Desviacion estandar: %f" %(std(tiempos)))