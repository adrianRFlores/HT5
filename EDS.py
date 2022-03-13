import simpy
import random
import math

procesos = int(input("Ingrese la cantidad de procesos: "))
procesosC = procesos
#intervalo = int(input("Ingrese el intervalo de entrada de procesos: "))
intervalo = 1
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

def genProceso(env, name, ram, cpu):
    global totalT
    
    expo = int(random.expovariate(1.0/intervalo))
    yield env.timeout(expo)
    
    instrucciones = random.randint(1, 10)
    mem = random.randint(1,10)
    tEntrada = env.now
    
    with ram.get(mem) as entrada:
        yield entrada        
        
        #Version uvg
        estado = 2
        while(instrucciones > 0):
                
            if(estado == 1):
                #print("%s IO" %name)
                with io.request() as waiting:
                    yield waiting
                    env.timeout(1)
                estado = 2    
            
            while((estado == 2) and (instrucciones > 0)):
                #print(name)
                with cpu.request() as activo:
                    yield activo
                    yield env.timeout(1)
                    instrucciones -= 3
                estado = random.randint(1,2)
        #Fin version uvg
        
        yield ram.put(mem)
       
    tfinal = env.now - tEntrada
    print(name + ": %d" %tfinal)
    tiempos.append(tfinal)
    totalT += tfinal

env = simpy.Environment()
ram = simpy.Container(env, init = 100, capacity = 100)
cpu = simpy.Resource(env, capacity = 1)
io = simpy.Resource(env)

totalT = 0
for i in range(procesos):
    env.process(genProceso(env, "proceso %d"%i, ram, cpu))

env.run()

print("\nTiempo total: %f" %totalT)
print("Tiempo promedio: %f" %(totalT/procesos))
print("Desviacion estandar: %f" %(std(tiempos)))