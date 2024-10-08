import numpy as np
from scipy.stats import skewnorm
from scipy.stats import truncpareto
from scipy.stats import vonmises_line

def intervaloDePedidoHamburguesa(p):
    a = 4.044016581362492
    loc =205.85701604001605
    scale = 100.42542523537097
    
    # Elasticidad no lineal: cuanto mayor sea el precio, más aumenta el intervalo de manera exponencial
    factor_precio = np.exp((PRECIO_DE_HAMBURGUESAS - PRECIO_BASE) / PRECIO_BASE)
    return skewnorm.ppf(p , a, loc, scale) * factor_precio

def intervaloDePedidoEnsalada(p):
    kappa = 0.04089227022947282
    loc =1890.0025157344721
    scale = 28.648690644317014
    return vonmises_line.ppf(p , kappa, loc, scale)
    
def intervaloDePedidoPapas(p):
    b = 22933.735496143887
    c = 1.0000013411007824
    loc = -134217740.8463965
    scale = 134218100.84639648
    return truncpareto.ppf(p, b, c, loc, scale)

def tiempoAtencionHamburguesa(p):
    return minutos_a_segundos(4*p + 8)

def tiempoAtencionEnsalada(p):
    return minutos_a_segundos(3*p + 8)

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


CANTIDAD_COCINEROS = 2
PRECIO_DE_HAMBURGUESAS = 9000
PRECIO_BASE = 10000
TF = minutos_a_segundos(60*4) #simulacion de 4 horas
DIAS_A_SIMULAR = 1600 #simulacion de 1600 dias 
CANTIDAD_FREIDORAS = 3
CAPACIDAD_PLANCHAS = 6

# Tiempos comprometidos (inicializados en 0 para cada estac1ión)
global tcf, tcp, tcc1, tcc2
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
stapf = [1] * CANTIDAD_FREIDORAS
stap = [1] * CAPACIDAD_PLANCHAS
stae = 0
stac1 = 0
stac2 = 0
stelp = 0
chul = 0

# Tiempo de limpieza de plancha
global tplp
tplp = 0

global flag, arrep, arrepPF
arrep = 0
arrepPF = 0
flag = 'Hamburguesa'

def main():
    dia = 0
    n = 0
    cantidad_pedidos_hamburugesa = 0
    cantidad_pedidos_papas = 0
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
                cantidad_pedidos_papas = cantidad_pedidos_papas + 1
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
    pepf = float(sum(stepf) / sum(ntpf))
    peh = float(steh / nth)
    print(f"peh = {steh} / {nth} = {peh}")
    pee = float(stee / nte)


    ptoc1 = float((stoc1*100) / (stoc1 + stac1))
    ptoc2 = float((stoc2*100) / (stoc2 + stac2))
    
    #ptoc = []
    #for i in range(0, len(stoc1)):
    #    ptoc.append((stoc1[i]*100) / stoc1[i] + stac1[i])
    
    ptop = []
    for i in range(0, len(stop)):
        ptop.append(float((stop[i]*100) / (stop[i] + stap[i])))

    ptof = []
    for i in range(0, len(stof)):
        ptof.append(float((stof[i]*100) / (stof[i] + stapf[i])))

    ptof2 = []
    for i in range(0, len(stof)):
        ptof2.append((stof[i]*100) / (stof[i] + stapf[i]))
    
    # Crear una lista de porcentajes formateados
    porcentajes_formateados2 = [f"{porcentaje:.2f}%" for porcentaje in ptof2]

    # Unir los porcentajes con comas y mostrarlos entre corchetes
    print(f"Porcentaje de tiempo ocioso de Freidoras: [{', '.join(porcentajes_formateados2)}]")

    #ptop1 = []
    #for i in range(len(stop)):
    #    ptop1.append((stop[i] * 100) / (stop[i] + stap[i]))

    # Formatear la salida con f-strings para limitar los decimales a 2
    #print("Porcentaje de tiempo ocioso de planchas:")
    #for porcentaje in ptop1:
    #    print(f"{porcentaje:.2f}%")

    ptop2 = []
    for i in range(len(stop)):
        ptop2.append((stop[i] * 100) / (stop[i] + stap[i]))

    # Crear una lista de porcentajes formateados
    porcentajes_formateados = [f"{porcentaje:.2f}%" for porcentaje in ptop2]

    # Unir los porcentajes con comas y mostrarlos entre corchetes
    print(f"Porcentaje de tiempo ocioso de planchas: [{', '.join(porcentajes_formateados)}]")

    print("Promedio de espera de Papas Fritas: ", segundosAMinutos(pepf))
    print("Promedio de espera de Hamburguesas: ", segundosAMinutos(peh))
    print("Promedio de espera de Ensaladas: ", segundosAMinutos(pee))
    print(f"Porcentaje de Tiempo Ocioso de Cocinero 1: {ptoc1:.2f}%")
    print(f"Porcentaje de Tiempo Ocioso de Cocinero 2: {ptoc2:.2f}%")
    print("Cantidad de Arrepentimientos H entre 10 y 20 minutos: ", contador20)
    print("Cantidad de Arrepentimientos H entre 20 y 40 minutos: ", contador40)
    print("Cantidad de Arrepentimientos H mas de 40 minutos: ", contadorMas40)
    print("Cantidad Total de Pedidos: ", n)
    print("Cantidad Pedidos de Hamburguesas:", contador20 + contador40 + contadorMas40 + nth)
    print("Cantidad de Hamburguesas hechas: ", nth)
    print(f"Porcentaje de Arrepentimientos entre 10 y 20 minutos:  {(contador20 * 100) / cantidad_pedidos_hamburugesa:.2f}%")
    print(f"Porcentaje de Arrepentimientos entre 20 y 40 minutos: {(contador40 * 100) / cantidad_pedidos_hamburugesa:.2f}%")
    print(f"Porcentaje de Arrepentimientos mas de 40 minutos: {(contadorMas40 * 100) / cantidad_pedidos_hamburugesa:.2f}%")
    print(f"Porcentaje de Pedidos de Hamburguesas que Hicimos: {(nth * 100) / cantidad_pedidos_hamburugesa:.2f}%")
    print(f"Ganancias con Hamburguesas: ${nth * 12000:,.0f}")
    print(f"Ganancias con Papas Fritas: ${(sum(ntpf) - (nth*0.8)) * 5000:,.0f}")

def preparacionPapasFritas(t):
    global tcf, stepf, stof, stapf, ntpf, arrepPF  
    
    i_freidora = tcf.index(min(tcf))  # Seleccionar la freidora con menor TCF
    tapf = tiempoAtencionPapasFritas(np.random.rand())

    if t <= tcf[i_freidora]:  # Freidora ocupada
        stepf[i_freidora] += (tcf[i_freidora] - t)  # Sumar al acumulador de espera
        tcf[i_freidora] += tapf  # Actualizar el tiempo comprometido
    else:  # Freidora disponible
        stof[i_freidora] += (t - tcf[i_freidora])  # Sumar al tiempo ocioso
        tcf[i_freidora] = t + tapf  # Actualizar el tiempo comprometido 
    stapf[i_freidora] += tapf
    ntpf[i_freidora] += 1  # Incrementar el contador de pedidos atendidos

def preparacionHamburguesa(t):
    global tcc1, stop, steh, stoc1, tcp, arrep, nth, stap, stac1, chul, tplp, flag, tcf, tcc2

    i_freidora = tcf.index(min(tcf))  # Seleccionar la freidora con menor TCF
    
    r = np.random.rand()

    i_plancha = tcp.index(min(tcp))  # Seleccionar la plancha con menor TCP
    tah = 0

    if r <= 0.8:
        maxTC = max(tcp[i_plancha], tcf[i_freidora])  
    else:
        maxTC = max(tcp[i_plancha], tcc2)  

    if tcp[i_plancha] > tcc1:
        if t <= tcp[i_plancha]:
            arrepentimiento = arrepentimientoRut(t, maxTC)
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
            tcc1 = t + tah
    else:
        if t <= tcp[i_plancha]:
            arrepentimiento = arrepentimientoRut(t, maxTC)
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
