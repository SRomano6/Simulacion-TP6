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

    return ("hola")


TIEMPO_ENTRE_LIMPIEZA_DE_PLANCHAS = minutos_a_segundos(15)
CANTIDAD_COCINEROS = 2
CAPACIDAD_PLANCHAS = 2
PRECIO_HAMBURGUESA = 200
TF = minutos_a_segundos(60*3.5) #simulacion de 3.5 horas
DIAS_A_SIMULAR = 25 #simulacion de 25 dias 

def main():
    dia = 0
    while(DIAS_A_SIMULAR < dia):
        t = 0
        while(t < TF):
            tpppf   = intervaloDePedidoPapas(np.random.rand()) + t
            tpph    = intervaloDePedidoHamburguesa(np.random.rand()) + t
            tppe    = intervaloDePedidoEnsalada(np.random.rand()) + t
            tplp    = intervaloLimpiezaDePlancha() + t
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




















 # Inicializar las variables necesarias
T = 0  # Tiempo actual en la simulación
TAPF = 7  # Tiempo de Atención Papas Fritas
TAH = 9  # Tiempo de Atención Hamburguesa
TAE = 5  # Tiempo de Atención Ensalada

# Tiempos comprometidos (inicializados en 0 para cada estación)
TCF = [0]  # Tiempo Comprometido Freidoras
TCP = [0]  # Tiempo Comprometido Planchas
TCC = [0]  # Tiempo Comprometido Cocineros

# Tiempos ociosos y de espera acumulados
STOF = [0]  # Tiempo Ocioso Freidoras
STOH = [0]  # Tiempo Ocioso Planchas
STOE = [0]  # Tiempo Ocioso Estación Ensaladas
STEPF = [0]  # Tiempo de Espera Papas Fritas
STEH = [0]  # Tiempo de Espera Hamburguesas
STEE = [0]  # Tiempo de Espera Ensaladas

# Contadores de pedidos atendidos
NTPF = 0  # Número total de pedidos de papas fritas atendidos
NTH = 0   # Número total de pedidos de hamburguesas atendidos
NTE = 0   # Número total de pedidos de ensaladas atendidos

# Función para procesar un pedido de papas fritas
def procesar_pedido_papas_fritas(T):
    i_freidora = TCF.index(min(TCF))  # Seleccionar la freidora con menor TCF
    GENERAR TAPF
    if T <= TCF[i_freidora]:  # Freidora ocupada
        STEPF[i] += (TCF[i_freidora] - T)  # Sumar al acumulador de espera
        TCF[i_freidora] += TAPF  # Actualizar el tiempo comprometido
    else:  # Freidora disponible
        STOF[i_freidora] += (T - TCF[i_freidora])  # Sumar al tiempo ocioso
        TCF[i_freidora] = T + TAPF  # Actualizar el tiempo comprometido
    
    STAPF += TAPF
    NTPF += 1  # Incrementar el contador de pedidos atendidos



# Función para procesar un pedido de hamburguesas
def procesar_pedido_hamburguesa(T):
    i_plancha = TCP.index(min(TCP))  # Seleccionar la plancha con menor TCP
    i_cocinero = TCC.index(min(TCC))  # Seleccionar el cocinero con menor TCC
    
    # Verificar si tanto la plancha como el cocinero están ocupados
    if T >= TCP[i_plancha] or T >= TCC[i_cocinero]: # Plancha y cocinero libres

        generar TAH

        STOP[i_plancha] += (T - TCP[i_plancha])  # Sumar al tiempo ocioso de la plancha
        STOC[i_cocinero] += (T - TCC[i_cocinero])  # Sumar al tiempo ocioso del cocinero
        TCP[i_plancha] = T + TAH  # Actualizar el tiempo comprometido de la plancha
        TCC[i_cocinero] = T + TAH  # Actualizar el tiempo comprometido del cocinero


        # Si alguno está ocupado, acumulamos el tiempo de espera
        STEH[i_plancha] += (max(TCH[i_plancha], TCC[i_cocinero]) - T)  # Sumar al acumulador de espera de hamburguesas
        TCP[i_plancha] += TAH  # Actualizar el tiempo comprometido de la plancha
        TCC[i_cocinero] += TAH  # Actualizar el tiempo comprometido del cocinero
    else:
        if T <= TCP[i_plancha]:
        Arrepentimiento
            if Arr == False:
            Generar TAH
                STEH[i_plancha] += (TCP[i_plancha] - T)  # Sumar al acumulador de espera de hamburguesas
                STOC[i_cocinero] += (TCP[i_plancha] - TCC[i_cocinero])  # Sumar al tiempo ocioso del cocinero
                TCP[i_plancha] =  TCP[i_plancha] + TAH  # Actualizar el tiempo comprometido de la plancha
                TCC[i_cocinero] =  TCP[i_plancha] + TAH  # Actualizar el tiempo comprometido del cocinero
            else: arrep += 1 break

        else if T <= TCC[i_cocinero]:
        Arrepentimiento
            if Arr == False:
                Generar TAH
                STEH[i_plancha] += (TCC[i_cocinero] - T)  # Sumar al acumulador de espera de hamburguesas
                STOP[i_plancha] += (TCC[i_cocinero] - TCP[i_plancha])  # Sumar al tiempo ocioso del cocinero
                TCP[i_plancha] =  TCC[i_cocinero] + TAH  # Actualizar el tiempo comprometido de la plancha
                TCC[i_cocinero] =  TCC[i_cocinero] + TAH  # Actualizar el tiempo comprometido del cocinero
            else: arrep += 1 break
        
    STAC[i_cocinero] = STAC[i_cocinero] + TAH
    STAP[i_plancha] = STAP[i_plancha] + TAH
    NTH += 1  # Incrementar el contador de pedidos de hamburguesas atendidos  
    CHUL += 1
    if CHUL >= 50:
        TPLP = TCP(i_plancha) #ACA NO SE DEBERIA PODER ATENDER NINGUNA HAMBURGUESSA MAS HASTA QUE SE LIMPIE

    random
    if r <= 0,8: 
       procesar_pedido_papas_fritas
    else
       procesar_pedido_ensalada
         

# Función para procesar un pedido de ensaladas
def procesar_pedido_ensalada(T):
    i_cocinero = TCC.index(min(TCC))  # Seleccionar el cocinero con menor TCC
    GENERAR TAE
    if T <= TCC[i_cocinero]:  # Cocineros ocupados
        STEE[i] += (TCC[i_cocinero] - T)  # Sumar al acumulador del cocinero
        TCC[i_cocinero] += TAE  # Actualizar el tiempo comprometido del Cocinero
    else:  # Cocinero libre
        STOC[i_cocinero] += (T - TCC[i_cocinero])  # Sumar al tiempo ocioso del Cocienro
        TCE[i_cocinero] = T + TAE  # Actualizar el tiempo comprometido
    STAC[i_cocinero] = STAC[i_cocinero] + TAE
    NTE += 1  # Incrementar el contador de pedidos de ensaladas atendidos



# Función para procesar Limpieza de Plancha
def procesar_limpieza_plancha(T):
    i_plancha = TCC.index(MAX(TCP))  # Seleccionar el cocinero con menor TCC
    GENERAR TALP
    if T <= TCP[i_plancha]:  # plancha ocupada
        TCP[1] = TCP(i) + TALP  # Actualizar el tiempo comprometido de la plancha
        TCP[2] = TCP(i) + TALP  # Actualizar el tiempo comprometido de la plancha
        TCP[3] = TCP(i) + TALP  # Actualizar el tiempo comprometido de la plancha
        TCP[4] = TCP(i) + TALP  # Actualizar el tiempo comprometido de la plancha
        TCP[5] = TCP(i) + TALP  # Actualizar el tiempo comprometido de la plancha
        TCP[6] = TCP(i) + TALP  # Actualizar el tiempo comprometido de la plancha
    else:  # Plancha libre
        TCP[1] = T + TALP  # Actualizar el tiempo comprometido de la plancha

    TPLP = TCP + 30
    CHUL = 0       