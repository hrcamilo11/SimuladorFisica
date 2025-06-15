import numpy as np

def calcular_pendulo_simple(longitud, angulo_inicial_rad, gravedad=9.81, tiempo_total_simulacion=None, num_puntos=200):
    """
    Calcula el movimiento de un péndulo simple usando la aproximación de ángulos pequeños (MAS).
    θ(t) = θ_max * cos(ωt + φ)
    ω = sqrt(g/L)
    Si no se da tiempo_total_simulacion, se calcula para dos periodos completos.
    """
    if longitud <= 0:
        raise ValueError("La longitud del péndulo debe ser positiva.")
    if tiempo_total_simulacion is not None and tiempo_total_simulacion <=0:
        raise ValueError("El tiempo total de simulación debe ser positivo si se provee.")
    # Para la aproximación de MAS, el ángulo inicial no debería ser muy grande.
    # No se impone un límite estricto aquí, pero la física es más precisa para |θ_inicial| < ~0.26 rad (15 grados)

    frecuencia_angular = np.sqrt(gravedad / longitud)
    periodo = 2 * np.pi / frecuencia_angular

    if tiempo_total_simulacion is None:
        tiempo_total_simulacion = 2 * periodo # Simular dos periodos por defecto
    
    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    
    # Asumimos que se suelta desde el reposo en angulo_inicial_rad, entonces φ=0 y θ_max = angulo_inicial_rad
    angulos_rad = angulo_inicial_rad * np.cos(frecuencia_angular * tiempos)
    velocidades_angulares = -angulo_inicial_rad * frecuencia_angular * np.sin(frecuencia_angular * tiempos)
    aceleraciones_angulares = -angulo_inicial_rad * (frecuencia_angular**2) * np.cos(frecuencia_angular * tiempos)
    # O: aceleraciones_angulares = -(frecuencia_angular**2) * angulos_rad

    # Posiciones cartesianas (opcional, pero útil para animación)
    # Origen en el punto de suspensión, y positivo hacia abajo
    pos_x = longitud * np.sin(angulos_rad)
    pos_y = -longitud * np.cos(angulos_rad) # y es negativo (hacia arriba desde el punto más bajo) o positivo (hacia abajo desde el pivote)
                                          # Si el pivote es (0,0), y= -Lcos(theta)

    # Combinar los estados en una lista de diccionarios para facilitar la animación
    estados_simulacion = [
        {"tiempo": t, "angulo_rad": ar, "velocidad_angular": va, "aceleracion_angular": aa, "posicion_x": px, "posicion_y": py}
        for t, ar, va, aa, px, py in zip(tiempos, angulos_rad, velocidades_angulares, aceleraciones_angulares, pos_x, pos_y)
    ]

    return list(tiempos), list(angulos_rad), list(velocidades_angulares), list(aceleraciones_angulares), list(pos_x), list(pos_y), periodo, frecuencia_angular, estados_simulacion