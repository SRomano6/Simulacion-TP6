import numpy as np
from scipy.stats import exponnorm
from scipy.stats import truncpareto
from scipy.stats import rel_breitwigner

def intervaloDePedidoHamburguesa(p):
    a = 4.651616792818317
    loc = 68.96346392723524
    scale = 12.76110784225058
    return exponnorm.ppf(p, a, loc, scale) 

def intervaloDePedidoEnsalada(p):
    return minutos_a_segundos(p*3 +10)
    

def intervaloDePedidoPapas(p):
    a = 22933.735496143887
    b = 1.0000013411007824
    loc = -134217740.8463965
    scale = 134218100.84639648
    return truncpareto.ppf(p ,a,b,  loc, scale)

def tiempoAtencionHamburguesa(p):
    return minutos_a_segundos(4*p + 20)

def tiempoAtencionEnsalada(p):
    return minutos_a_segundos(3*p + 4)

def tiempoAtencionPapasFritas(p):
    return minutos_a_segundos(3*p + 8)

def tiempoLimpiezaPlancha(p):
    return minutos_a_segundos(5*p + 5)

def minutos_a_segundos(minutos):
    return minutos * 60

def segundosAMinutos(segundos):
    return segundos / 60

def intervaloLimpiezaDePlancha():
    return minutos_a_segundos(30)

    
def proximoEvento2(proximoPedido):
    # Encuentra el evento con el menor tiempo en el diccionario
    evento = min(proximoPedido, key=proximoPedido.get)
    
    # Devuelve el nombre del evento con el menor tiempo
    return evento


CANTIDAD_COCINEROS = 1
PRECIO_HAMBURGUESA = 200
TF = minutos_a_segundos(60*3.5) #simulacion de 3.5 horas
DIAS_A_SIMULAR = 10 #simulacion de 25 dias 
CANTIDAD_FREIDORAS = 3
CAPACIDAD_PLANCHAS = 6

# Tiempos comprometidos (inicializados en 0 para cada estac1ión)
global tcf, tcp, tcc1
tcf = [0] * CANTIDAD_FREIDORAS  # Tiempo Comprometido Freidoras (una lista de ceros del tamaño de las freidoras)
tcp = [0] * CAPACIDAD_PLANCHAS  # Tiempo Comprometido Planchas (una lista de ceros del tamaño de las planchas)
tcc1 = 0  
tcc2 = 0  

# Tiempos ociosos y de espera acumulados
global stof, stop, stoe, stoc1, stepf, steh, stee
stof = [0] * CANTIDAD_FREIDORAS  # Tiempo Ocioso Freidoras
stop = [0] * CAPACIDAD_PLANCHAS   # Tiempo Ocioso Planchas
stoe = 0   # Tiempo Ocioso Estac1ión Ensaladas (solo una estac1ión de ensaladas)
stoc1 = 0   # Tiempo Ocioso Cocineros (un cocinero)
stoc2 = 0
stepf = [0] * CANTIDAD_FREIDORAS  # Tiempo de Espera Papas Fritas
steh = 0  # Tiempo de Espera Hamburguesas
stee = 0  # Tiempo de Espera Ensaladas

# Contadores de pedidos atendidos
global ntpf, nth, nte
ntpf = [0] * CANTIDAD_FREIDORAS  # Número total de pedidos de papas fritas atendidos por freidora
nth = 0  # Número total de pedidos de hamburguesas atendidos
nte = 0  # Número total de pedidos de ensaladas atendidos

# Sumatorias
global stapf, stap, stae, stac1, stelp, chul
stapf = [0] * CANTIDAD_FREIDORAS
stap = [0] * CAPACIDAD_PLANCHAS
stae = 0
stac1 = 0
stac2 = 0
stelp = 0
chul = 0

# Tiempo de limpieza de plancha
global tplp
tplp = 0

global flag, arrep
arrep = 0
flag = 'Hamburguesa'

def main():
    dia = 0
    n = 0
    cantidad_pedidos_hamburugesa = 0
    while(DIAS_A_SIMULAR > dia):
        global tcf, tcp, tcc1, tcc2, chul

        tcf = [0] * CANTIDAD_FREIDORAS
        tcp = [0] * CAPACIDAD_PLANCHAS
        tcc1 = 0
        tcc2 = 0
        chul = 0

        t = 0
        tpppf   = intervaloDePedidoPapas(np.random.rand()) 
        tpph    = intervaloDePedidoHamburguesa(np.random.rand()) 
        tppe    = intervaloDePedidoEnsalada(np.random.rand()) 
        tplp    = intervaloLimpiezaDePlancha()
        while(t < TF):
            n = n+1
            proximoPedido = {'Hamburguesa': tpph, 'Ensalada': tppe, 'Papas Fritas': tpppf, 'Limpieza de Plancha': tplp}
            proximoEvento = proximoEvento2(proximoPedido)
            
            if(proximoEvento == "Papas Fritas"):
                t = tpppf
                tpppf = intervaloDePedidoPapas(np.random.rand()) + t
                preparacionPapasFritas(t)
            elif(proximoEvento == "Hamburguesa"):
                cantidad_pedidos_hamburugesa = cantidad_pedidos_hamburugesa + 1
                t = tpph
                tpph = intervaloDePedidoHamburguesa(np.random.rand()) + t
                preparacionHamburguesa(t)
            elif(proximoEvento == "Ensalada"):
                t = tppe
                tppe = intervaloDePedidoEnsalada(np.random.rand()) + t
                preparacionEnsalada(t)
            elif(proximoEvento == "Limpieza de Plancha"):
                t = tplp
                tplp = t + intervaloLimpiezaDePlancha()
                preparacionLimpiezaPlancha(t)
        dia = dia + 1
    pepf = sum(stepf) / sum(ntpf)
    peh = steh / nth
    print(f"peh = {steh} / {nth} = {peh}")
    pee = stee / nte


    ptoc1 = (stoc1*100) / (stoc1 + stac1)
    ptoc2 = (stoc2*100) / (stoc2 + stac2)
    
    #ptoc = []
    #for i in range(0, len(stoc1)):
    #    ptoc.append((stoc1[i]*100) / stoc1[i] + stac1[i])
    
    ptop = []
    for i in range(0, len(stop)):
        ptop.append((stop[i]*100) / (stop[i] + stap[i]))

    ptof = []
    for i in range(0, len(stof)):
        ptof.append((stof[i]*100) / (stof[i] + stapf[i]))

    print("Promedio de espera de papas fritas: ", segundosAMinutos(pepf))
    print("Promedio de espera de hamburguesas: ", segundosAMinutos(peh))
    print("Promedio de espera de ensaladas: ", segundosAMinutos(pee))
    print("Porcentaje de tiempo ocioso de cocineros1: ", ptoc1)
    print("Porcentaje de tiempo ocioso de cocineros2: ", ptoc2)
    print("Porcentaje de tiempo ocioso de planchas: ", ptop)
    print("Porcentaje de tiempo ocioso de freidoras: ", ptof)
    print("Cantidad de arrepentimientos entre 10 y 20 minutos: ", contador20)
    print("Cantidad de arrepentimientos entre 20 y 40 minutos: ", contador40)
    print("Cantidad de arrepentimientos mas de 40 minutos: ", contadorMas40)
    print("cantidad hamburguesas:", contador20 + contador40 + contadorMas40 + nth)
    print("n: ", n)
    print("nth: ", nth)
    print("Porcentaje de arrepentimientos entre 10 y 20 minutos: ", (contador20 * 100) / cantidad_pedidos_hamburugesa)
    print("Porcentaje de arrepentimientos entre 20 y 40 minutos: ", (contador40 * 100) / cantidad_pedidos_hamburugesa)
    print("Porcentaje de arrepentimientos mas de 40 minutos: ", (contadorMas40 * 100) / cantidad_pedidos_hamburugesa)
    print("Porcentaje de pedidos de Hamburguesas que Hicimos: ", (nth * 100) / cantidad_pedidos_hamburugesa)

def preparacionPapasFritas(t):
    global tcf, stepf, stof, stapf, ntpf  
    
    i_freidora = tcf.index(min(tcf))  # Seleccionar la freidora con menor TCF
    tapf  = tiempoAtencionPapasFritas(np.random.rand())
    if t <= tcf[i_freidora]:  # Freidora ocupada
        stepf[i_freidora] += (tcf[i_freidora] - t)  # Sumar al acumulador de espera
        tcf[i_freidora] += tapf  # Actualizar el tiempo comprometido
    else:  # Freidora disponible
        stof[i_freidora] += (t - tcf[i_freidora])  # Sumar al tiempo ocioso
        tcf[i_freidora] = t + tapf  # Actualizar el tiempo comprometido 
    stapf[i_freidora] += tapf
    ntpf[i_freidora] += 1  # Incrementar el contador de pedidos atendidos

def preparacionHamburguesa(t):
    global tcc1, stop, steh, stoc1, tcp, arrep, nth, stap, stac1, chul, tplp, flag

    i_plancha = tcp.index(min(tcp))  # Seleccionar la plancha con menor TCP
    tah = 0 
    if tcp[i_plancha] > tcc1:
        if t <= tcp[i_plancha]:
            arrepentimiento = arrepentimientoRut(t, tcp[i_plancha])
            if not arrepentimiento:
                tah = tiempoAtencionHamburguesa(np.random.rand())
                stoc1 = stoc1 + (tcp[i_plancha] - tcc1) 
                steh = steh + (tcp[i_plancha] - t)
                tcp[i_plancha] = tcp[i_plancha] + tah
                tcc1 = tcp[i_plancha] + tah
            else:
                arrep = arrep + 1
                return
        else:
            tah = tiempoAtencionHamburguesa(np.random.rand())
            stoc1 = stoc1 + (t - tcc1)
            stop[i_plancha] = stop[i_plancha] + (t - tcp[i_plancha])
            tcp[i_plancha] = t + tah

    else:
        if t <= tcp[i_plancha]:
            arrepentimiento = arrepentimientoRut(t, tcp[i_plancha])
            if not arrepentimiento:
                tah = tiempoAtencionHamburguesa(np.random.rand())
                steh = steh + (tcp[i_plancha] - t)
                tcp[i_plancha] = tcp[i_plancha] + tah
                tcc1 = tcp[i_plancha] + tah
            else:
                arrep = arrep + 1
                return
        else:
            tah = tiempoAtencionHamburguesa(np.random.rand())
            stop[i_plancha] = stop[i_plancha] + (t - tcp[i_plancha])
            tcp[i_plancha] = t + tah
            tcc1 = t + tah

    stac1 = stac1 + tah
    stap[i_plancha] = stap[i_plancha] + tah
    nth = nth + 1  
    chul = chul + 1
    flag = 'Hamburguesa'
    if chul >= 50:
        talp = tiempoLimpiezaPlancha(np.random.rand())
        for i in range(0, len(tcp)):
            tcp[i] = tcp[tcp.index(max(tcp))] + talp
        tplp = tcp[i_plancha] + intervaloLimpiezaDePlancha()
        chul = 0
    r = np.random.rand()
    if r <= 0.8: 
        preparacionPapasFritas(t)
    else:
        preparacionEnsalada(t)

def preparacionEnsalada(t):
    global tcc2, stee, stac2, nte, stoc2

    tae = tiempoAtencionEnsalada(np.random.rand())
    if t <= tcc2:
        stee = stee + (tcc2 - t)
        tcc2 = tcc2 + tae
    else:
        stoc2 = stoc2 + (t - tcc2)
        tcc2 = t + tae
    stac2 = stac2 + tae
    nte = nte + 1  

def preparacionLimpiezaPlancha(t):
    global tcp, stelp, stop, chul

    i_plancha_mayor = tcp.index(max(tcp)) 
    talp = tiempoLimpiezaPlancha(np.random.rand())
    if t <= tcp[i_plancha_mayor]:
        stelp = stelp + (tcp[i_plancha_mayor] - t)
        for i in range(0, len(tcp)):
            tcp[i] = tcp[i_plancha_mayor] + talp
    else:
        for i in range(0, len(tcp)):
            stop[i] = stop[i] + (t - tcp[i])
            tcp[i] = t + talp
    chul = 0

global contador20, contador40, contadorMas40
contador20 = 0
contador40 = 0
contadorMas40 = 0
def arrepentimientoRut(t, tc):
    global contador20, contador40, contadorMas40
    espera = tc - t
    if espera <= minutos_a_segundos(10):
        return False
    else:
        if espera <= minutos_a_segundos(20):
            r = np.random.rand()
            if r <= 0.7:
                return False
            else:
                contador20 = contador20 + 1
                return True
        else:
            if espera <= minutos_a_segundos(40):
                r = np.random.rand()
                if r <= 0.2:
                    return False
                else:
                    contador40 = contador40 + 1
                    return True
            else:
                contadorMas40 = contadorMas40 + 1 
                return True
        
if __name__ == "__main__":
    main()
