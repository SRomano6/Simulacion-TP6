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
            tpppf   = intervaloDePedidoPapas(np.random.rand(0.1 , 0.9)) + t
            tpph    = intervaloDePedidoHamburguesa(np.random.rand(0.1 , 0.9)) + t
            tppe    = intervaloDePedidoEnsalada(np.random.rand(0.1 , 0.9)) + t
            tplp    = intervaloLimpiezaDePlancha() + t
            proximoPedido = {'Hamburguesa': tpph, 'Ensalada': tppe, 'Papas Fritas': tpppf, 'Limpieza de Plancha': tplp}
            
            proximoEvento = proximoEventoTC(proximoPedido)
            
            if(proximoEvento == "Papas Fritas"):
                t = tpppf
                tpppf = intervaloDePedidoPapas(np.random.rand(0.1 , 0.9)) + t
                preparacionPapasFritas(t)
            elif(proximoEvento == "Hamburguesa"):
                t = tpph
                tpph = intervaloDePedidoHamburguesa(np.random.rand(0.1 , 0.9)) + t
                preparacionHamburguesa(t)
            elif(proximoEvento == "Ensalada"):
                t = tppe
                tppe = intervaloDePedidoEnsalada(np.random.rand(0.1 , 0.9)) + t
                preparacionEnsalada(t)


        