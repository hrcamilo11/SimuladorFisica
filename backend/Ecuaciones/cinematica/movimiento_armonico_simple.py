import numpy as np

def calcular_movimiento_armonico_simple(amplitud, frecuencia_angular, fase_inicial, tiempo_total_simulacion, num_puntos=100):
    """
    Calcula la posición, velocidad y aceleración de un objeto en Movimiento Armónico Simple.
    x(t) = A * cos(ω*t + φ)
    v(t) = -Aω * sin(ω*t + φ)
    a(t) = -Aω^2 * cos(ω*t + φ) = -ω^2 * x(t)
    """
    if amplitud <= 0:
        raise ValueError("La amplitud debe ser positiva.")
    if frecuencia_angular <= 0:
        raise ValueError("La frecuencia angular (ω) debe ser positiva.")
    if tiempo_total_simulacion <= 0:
        raise ValueError("El tiempo total de simulación debe ser positivo.")

    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    
    posiciones = amplitud * np.cos(frecuencia_angular * tiempos + fase_inicial)
    velocidades = -amplitud * frecuencia_angular * np.sin(frecuencia_angular * tiempos + fase_inicial)
    aceleraciones = -amplitud * (frecuencia_angular**2) * np.cos(frecuencia_angular * tiempos + fase_inicial)
    # Alternativamente: aceleraciones = -(frecuencia_angular**2) * posiciones

    periodo = 2 * np.pi / frecuencia_angular
    frecuencia_hz = 1 / periodo

    # Combinar los estados en una lista de diccionarios para facilitar la animación
    estados_simulacion = [
        {"tiempo": t, "posicion": p, "velocidad": v, "aceleracion": a}
        for t, p, v, a in zip(tiempos, posiciones, velocidades, aceleraciones)
    ]

    return list(tiempos), list(posiciones), list(velocidades), list(aceleraciones), periodo, frecuencia_hz, estados_simulacion