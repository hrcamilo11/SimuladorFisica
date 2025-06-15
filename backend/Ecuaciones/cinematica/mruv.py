import numpy as np
from .ecuaciones_cinematica import calcular_posicion_final_tiempo, calcular_velocidad_final_tiempo

def calcular_mruv(posicion_inicial, velocidad_inicial, aceleracion, tiempo_total, num_puntos=100):
    """
    Calcula la posición y velocidad de un objeto en Movimiento Rectilíneo Uniformemente Variado (MRUV).
    x(t) = x0 + v0*t + 0.5*a*t^2
    v(t) = v0 + a*t
    """
    if tiempo_total is None or not isinstance(tiempo_total, (int, float)):
        raise ValueError("El tiempo total debe ser un número válido.")
    if tiempo_total < 0:
        raise ValueError("El tiempo total no puede ser negativo.")
    if num_puntos <= 1 and tiempo_total > 0:
        num_puntos = 2
    elif num_puntos < 1:
        num_puntos = 1

    tiempos = np.linspace(0, tiempo_total, num_puntos)
    posiciones = [calcular_posicion_final_tiempo(posicion_inicial, velocidad_inicial, aceleracion, t) for t in tiempos]
    velocidades = [calcular_velocidad_final_tiempo(velocidad_inicial, aceleracion, t) for t in tiempos]
    # Combinar los estados en una lista de diccionarios para facilitar la animación
    estados_simulacion = [
        {"tiempo": t, "posicion": p, "velocidad": v}
        for t, p, v in zip(tiempos, posiciones, velocidades)
    ]

    return list(tiempos), list(posiciones), list(velocidades), estados_simulacion