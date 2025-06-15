import math
from backend.Ecuaciones.electricidad_y_magnetismo.magnetismo import calcular_campo_magnetico, calcular_fuerza_lorentz, calcular_flujo_magnetico, calcular_ley_faraday

def simular_campo_magnetico(corriente, distancia):
    return calcular_campo_magnetico(corriente, distancia)

def simular_flujo_magnetico(campo_magnetico, area, angulo):
    return calcular_flujo_magnetico(campo_magnetico, area, angulo)

def simular_fuerza_lorentz(carga, velocidad, campo_magnetico, angulo):
    return calcular_fuerza_lorentz(carga, velocidad, campo_magnetico, angulo)

def simular_ley_faraday(num_espiras, flujo_magnetico_inicial, flujo_magnetico_final, tiempo):
    return calcular_ley_faraday(num_espiras, flujo_magnetico_inicial, flujo_magnetico_final, tiempo)