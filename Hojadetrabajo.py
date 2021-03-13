#Referencia: Ejemplo expuesto en clase
#Integrantes: Marco Orozco
#             Javier Valle

import simpy
import random
#Variables globales para controlar los aspectos
global CPUdisp
CPUdisp = 3
# Cada proceso sera un objeto, para facilitar el proceso
# En este caso, se llamara tarea, cada tarea tendra propiedades
# Ramtotal = container
# procesador = resource
# instrucciones = int cantidad de instrucciones de la tarea
# name = string nomrbe de la tarea
# tLleg = tiempo de llegada
# esp = resource
def nuevo (env,RAMtotal,procesador,instrucciones,name,tLleg,esp):

    ## Propiedades de cada clase
    global RAMnecesario,wait,esptot

    #Cantidad de memoria RAM que usa cada proceso, es aleatorio
    RAMnecesario = random.randint(1,10)

    #Hasta que haya memoria disponible, se accede a dejar pasar a la tarea
    with RAMtotal.get(RAMnecesario) as req:
        yield req #Esperando a que se complete la solicitud hacia la RAM
        
    print('%s Memoria RAM libre: %s RAM asignado:%s Instrucciones:%s \n' % (name,RAMtotal.level,RAMnecesario,instrucciones))
    ## El proceso pasa a ser un objeto ready
    ## La tarea se encuentra en estado ready
    d = listo(env,procesador,instrucciones,name,RAMnecesario,tLleg,esp)

    # El proceso se corre en este caso, se corre el proceso listo
    env.process(d)

# Este es un objeto tipo ready
# prcesador = resource
# instrucciones = int cantidad de instrucciones
# name = nombre de la tarea
# Ramnecesario = int ram que necesita el proceso
# tLleg = int tiempo en que llego a este estado
# esp = resource
# CPUdisp = cantidad de instrucciones permitidas por el procesador
def listo(env,procesador,instrucciones,name,RAMnecesario,tLleg,esp):

    #Variable que guarda la espera total
        global esptot

        #Se cumplen solo 3 instrucciones
        while instrucciones > 3:
            # Se pide acceder al procesador, y se deja pasar hasta que este disponible
            with procesador.request() as reqProcesador:
                yield reqProcesador #Esperando a que el procesador apruebe la solicitud realizada.
                yield env.timeout(1)

                # Se muestran las intrucciones que quedan de la tarea que se encuentra en proceso por el CPU
                print ('%s Instrucciones restantes:%s \n'%(name,instrucciones))

                #se resta la cant de instrucciones q hace la CPU por unidad de tiempo
                instrucciones = instrucciones - CPUdisp

                # El siguiente toma un proceso aleatorio
                siguiente = random.choice(["listo","en espera"])

                if siguiente == "en espera":
                    ##Si espera pasa al siguiente estado
                    print 
                    with esp.request() as reqesp:
                        yield reqesp
                        yield env.timeout(5)
                    
        with RAM.put(RAMnecesario) as req:
            yield req
        
        # Por ultimo se escribe la infomracion del proceso
        wait = env.now - tLleg
        esptot = esptot + wait
        print (name,'Ha terminado','Tiempo en que termino: ',wait)

# Ramtotal = container
# procesador = resource
# intervalo = float frecuencia en la que sale cad aproceso
#Procesos = numero de procesos que llegaran al CPU
# espera = resource
def inicio(env,RAMtotal,procesador,intervalo,procesos,espera):
    # se realiza la cantidad de veces dependiendo de la cantida de procesos que insertemos
    for i in range(procesos):
        #Se guarda el timepo de llegada
        tLlegada = env.now

        #Cantidad de instrucciones que tiene el proceso
        instrucciones = random.randint(1,10)

        # Se genera el proceso
        c = nuevo(env,RAMtotal,procesador,instrucciones,'Proceso %02d' % i,tLlegada,espera)
        env.process(c) #Procesando

        #Frecuencia de llegada de cada proceso
        t = random.expovariate(1.0/intervalo)

        #Espera el tiempo para el siguiente proceso
        yield env.timeout(t)
            


# Variables para probar
# Frecuencia en la qie tardan aparecer los procesos
frecuenciaProcesos = 1
randomSeed = 10
#Cantidad de procesos que seran insertados
cantidadProcesos = 150

#comienza la simulacion
random.seed(randomSeed)
env = simpy.Environment()
instrucciones = 0
esptot = 0.0

#ejecutar la simulacion e iniciar los recursos
procesador = simpy.Resource(env, capacity=1)
RAM = simpy.Container(env, init=100, capacity=100)
esp = simpy.Resource(env, capacity=1)


env.process(inicio(env,RAM,procesador, frecuenciaProcesos,cantidadProcesos,esp)) #Procesando el inicio.
env.run()

# Datos estadísticos
print ('Tiempo total',esptot,'Promedio de tiempo total: ',esptot / cantidadProcesos)