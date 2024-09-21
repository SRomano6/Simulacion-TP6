import numpy as np
from scipy.stats import pearson3
from scipy.stats import wald
from scipy.stats import rel_breitwigner

def intervaloDePedidoHamburguesa(p):
    loc = -60.91163336519913
    scale = 562.8685676898285
    return wald.ppf(p, loc, scale) 

def intervaloDePedidoEnsalada(p):
    a = 0.5480412546272729
    loc = -4.6239051501572844e-11
    scale = 436.9927972206234
    return rel_breitwigner.ppf(p, a, loc, scale)

def intervaloDePedidoPapas(p):
    a = 2.209810337576271
    loc = 1766.4765414991225
    scale = 1786.0532859271495
    return pearson3.ppf(p, a, loc, scale)

def tiempoAtencioHamburguesa(p):
    return minutos_a_segundos(4*p + 6)

def tiempoAtencionEnsalada(p):
    return minutos_a_segundos(3*p + 4)

def tiempoAtencionPapasFritas(p):
    return minutos_a_segundos(5*p + 10)

def minutos_a_segundos(minutos):
    return minutos * 60

def intervaloLimpiezaDePlancha():
    return minutos_a_segundos(30)

def proximoEventoTC(proximoPedido):
    if(proximoPedido['Hamburguesa'] < proximoPedido['Ensalada'] and proximoPedido['Hamburguesa'] < proximoPedido['Papas Fritas']):
        return ("Hamburguesa")
    elif(proximoPedido['Ensalada'] < proximoPedido['Hamburguesa'] and proximoPedido['Ensalada'] < proximoPedido['Papas Fritas']):
        return ("Ensalada")
    elif(proximoPedido['Papas Fritas'] < proximoPedido['Hamburguesa'] and proximoPedido['Papas Fritas'] < proximoPedido['Ensalada']):
        return ("Papas Fritas")
    else:
        return ("Limpieza de Plancha")



TIEMPO_ENTRE_LIMPIEZA_DE_PLANCHAS = minutos_a_segundos(15)
CANTIDAD_COCINEROS = 2
CAPACIDAD_PLANCHAS = 2
PRECIO_HAMBURGUESA = 200
TF = minutos_a_segundos(60*3.5) #simulacion de 3.5 horas
DIAS_A_SIMULAR = 25 #simulacion de 25 dias 

# Tiempos comprometidos (inicializados en 0 para cada estación)
tcf = [0]  # Tiempo Comprometido Freidoras
tcp = [0]  # Tiempo Comprometido Planchas
tcc = 0  # Tiempo Comprometido Cocineros

# Tiempos ociosos y de espera acumulados
stof = [0]  # Tiempo Ocioso Freidoras
stoh = [0]  # Tiempo Ocioso Planchas
stoe = [0]  # Tiempo Ocioso Estación Ensaladas
stoc = 0    # Tiempo Ocioso Cocineros
stop = [0]
stepf = [0]  # Tiempo de Espera Papas Fritas
steh = [0]  # Tiempo de Espera Hamburguesas
stee = [0]  # Tiempo de Espera Ensaladas

# Contadores de pedidos atendidos
ntpf = [0]  # Número total de pedidos de papas fritas atendidos
nth = 0   # Número total de pedidos de hamburguesas atendidos
nte = 0   # Número total de pedidos de ensaladas atendidos

# Sumatorias
stapf = 0
stap = 0
stae = 0
stac = 0
stelp = 0

# Arrepentimientos
arrep = 0

def main():
    dia = 0
    while(DIAS_A_SIMULAR < dia):
        t = 0
        tpppf   = intervaloDePedidoPapas(np.random.rand()) 
        tpph    = intervaloDePedidoHamburguesa(np.random.rand()) 
        tppe    = intervaloDePedidoEnsalada(np.random.rand()) 
        tplp    = intervaloLimpiezaDePlancha()
        while(t < TF):
            proximoPedido = {'Hamburguesa': tpph, 'Ensalada': tppe, 'Papas Fritas': tpppf, 'Limpieza de Plancha': tplp}
            proximoEvento = proximoEventoTC(proximoPedido)
            
            if(proximoEvento == "Papas Fritas"):
                t = tpppf
                tpppf = intervaloDePedidoPapas(np.random.rand()) + t
                preparacionPapasFritas(t)
            elif(proximoEvento == "Hamburguesa"):
                t = tpph
                tpph = intervaloDePedidoHamburguesa(np.random.rand()) + t
                preparacionHamburguesa(t)
            elif(proximoEvento == "Ensalada"):
                t = tppe
                tppe = intervaloDePedidoEnsalada(np.random.rand()) + t
                preparacionEnsalada(t)



def preparacionPapasFritas(t):
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
    i_plancha = tcp.index(min(TCP))  # Seleccionar la plancha con menor TCP
    tah = tiempoAtencioHamburguesa(np.random.rand())
    
    if tcp[i_plancha] > tcc:
        if t <= tcp[i_plancha]:
            arrepentimiento = arrepentimientoRut()
            if not arrepentimiento:
                tah = tiempoAtencioHamburguesa(np.random.rand())
                stoc = stoc + (tcp[i_plancha] - tcc) 
                steh = steh + (tcp[i_plancha] - t)
                tcp[i_plancha] = tcp[i_plancha] + tah
                tcc = tcp[i_plancha] + tah
            else:
                arrep = arrep + 1
                pass
        elif t <= tcc:
            arrepentimiento = arrepentimientoRut()
            if not arrepentimiento:
                tah = tiempoAtencioHamburguesa(np.random.rand())
                stop[i_plancha] = stop[i_plancha] + (tcc - tcp[i_plancha])
                steh = steh + (tcc - t)
                tcp[i_plancha] = tcc + tah
                tcc = tcc + tah
            else:
                arrep = arrep + 1
                pass
    else:
        tiempoAtencioHamburguesa(np.random.rand())
        stoc = stoc + (t - tcc)
        stop = stop + (t - tcp[i_plancha])
        tcp[i_plancha] = t + tah
    stac = stac + tah
    stap = stap + tah
    nth = nth + 1  
    chul = chul + 1
    if chul >= 50:
        talp = TIEMPO_ENTRE_LIMPIEZA_DE_PLANCHAS #cambiar
        for i in range(0, len(tcp)):
            tcp[i] = tcp[i] + talp
        talp = tcp + 30
        chul = 0
    r = np.random.rand()
    if r <= 0.8: 
        preparacionPapasFritas(t)
    else:
        preparacionEnsalada(t)

def preparacionEnsalada(t):
    tae = tiempoAtencionEnsalada(np.random.rand())
    if t <= tcc:
        stee = stee + (tcc - t)
        tcc = tcc + tae
    else:
        stoc = stoc + (t - tcc)
        tcc = t + tae
    stac = stac + tae
    nte = nte + 1  

def preparacionLimpiezaPlancha(t):
    i_plancha = tcp.index(min(TCP))  
    talp = intervaloLimpiezaDePlancha()
    if t <= tcp[i_plancha]:
        tcp[i_plancha] = tcp[i_plancha] + talp
        stelp = stelp + (tcp[i_plancha] - t)
    else:
        tcp[i_plancha] = t + talp
        stop = stop + (t - tcp[i_plancha])
    chul = 0

def arrepentimientoRut(t, tc):
    espera = tc - t
    if espera <= 10:
        return False
    else:
        if espera <= 20:
            r = np.random.rand()
            if r <= 0.7:
                return False
            else:
                return True
        else:
            if espera <= 40:
                r = np.random.rand()
                if r <= 0.2:
                    return False
                else:
                    return True
            else: 
                return True
        