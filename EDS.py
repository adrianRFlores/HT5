import simpy
import random
import math

procesos = int(input("Ingrese la cantidad de procesos: "))
procesosC = procesos
#intervalo = int(input("Ingrese el intervalo de entrada de procesos: "))
intervalo = 10
tiempos = []
random.seed(10)

def std(data):
    n = len(data)
    # Mean of the data
    mean = sum(data) / n
    # Square deviations
    deviations = [(x - mean) ** 2 for x in data]
    # Variance
    variance = sum(deviations) / n
    return math.sqrt(variance)

def genProceso(env, env1, name, ram, cpu):
    global totalT
    
    expo = random.expovariate(1.0/intervalo)
    yield env.timeout(expo)
    
    instrucciones = random.randint(1, 10)
    instruccionesIniciales = instrucciones
    
    with ram.get(instrucciones) as entrada:
        yield entrada
        entrada = env.now
        
        with cpu.request() as activo:
            yield activo
                    
            #Version simple
            while(instrucciones > 0):
                yield env.timeout(1)
                instrucciones -= 3
            #Fin version simple
        
        yield ram.put(instruccionesIniciales)
       
    tfinal = env.now - entrada
    print(name + ": %d" %tfinal)
    tiempos.append(tfinal)
    totalT += tfinal

env = simpy.Environment()
envIO = simpy.Environment()
ram = simpy.Container(env, init = 100, capacity = 100)
cpu = simpy.Resource(env, capacity = 2)
io = simpy.Resource(envIO)

totalT = 0
for i in range(procesos):
    env.process(genProceso(env, envIO, "proceso %d"%i, ram, cpu))
    
#while procesosC > 0:
    

env.run()

print("\nTiempo total: %f" %totalT)
print("Tiempo promedio: %f" %(totalT/procesos))
print("Desviacion estandar: %f" %(std(tiempos)))