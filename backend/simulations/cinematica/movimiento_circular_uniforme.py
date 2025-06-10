import numpy as np

def calcular_movimiento_circular_uniforme(radio, velocidad_angular=None, velocidad_tangencial=None, tiempo_total_simulacion=None, num_puntos=100):
    """
    Calcula la trayectoria de un objeto en Movimiento Circular Uniforme.
    Se debe proveer radio y (velocidad_angular O velocidad_tangencial).
    Si no se da tiempo_total_simulacion, se calcula para una vuelta completa.
    Retorna tiempos, angulos_rad, posiciones_x, posiciones_y, aceleracion_centripeta.
    """
    if radio <= 0:
        raise ValueError("El radio debe ser positivo.")

    if velocidad_angular is None and velocidad_tangencial is None:
        raise ValueError("Se debe proveer velocidad_angular o velocidad_tangencial.")
    if velocidad_angular is not None and velocidad_tangencial is not None:
        # Verificar consistencia si se dan ambas, o priorizar una. Priorizamos angular.
        if not np.isclose(velocidad_tangencial, velocidad_angular * radio):
            # Podríamos recalcular v_t o lanzar error. Por ahora, recalculamos v_t basado en omega.
            velocidad_tangencial = velocidad_angular * radio
            # raise ValueError("Velocidad angular y tangencial inconsistentes.")
    elif velocidad_angular is None:
        if radio == 0: raise ValueError("Radio no puede ser cero si solo se da velocidad tangencial")
        velocidad_angular = velocidad_tangencial / radio
    elif velocidad_tangencial is None:
        velocidad_tangencial = velocidad_angular * radio

    if velocidad_angular == 0: # No hay movimiento circular si omega es 0
        # Podríamos simular un punto estático o devolver error/vacío
        tiempos = np.linspace(0, tiempo_total_simulacion if tiempo_total_simulacion else 1, num_puntos)
        angulos = np.zeros(num_puntos)
        pos_x = np.full(num_puntos, radio) # Asumimos en (r,0) inicialmente
        pos_y = np.zeros(num_puntos)
        return list(tiempos), list(angulos), list(pos_x), list(pos_y), 0.0

    if tiempo_total_simulacion is None:
        # Tiempo para una vuelta completa: T = 2*pi / omega
        if velocidad_angular == 0: tiempo_total_simulacion = 1 # Evitar división por cero, aunque ya cubierto arriba
        else: tiempo_total_simulacion = 2 * np.pi / abs(velocidad_angular)
    
    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    angulos_rad = velocidad_angular * tiempos  # Asumimos ángulo inicial = 0
    
    posiciones_x = radio * np.cos(angulos_rad)
    posiciones_y = radio * np.sin(angulos_rad)
    
    aceleracion_centripeta = (velocidad_tangencial**2) / radio if radio > 0 else 0
    # O también: aceleracion_centripeta = (velocidad_angular**2) * radio

    # Combinar los estados en una matriz para facilitar la animación
    estados_simulacion = np.array([tiempos, angulos_rad, posiciones_x, posiciones_y]).T.tolist()

    return list(tiempos), list(angulos_rad), list(posiciones_x), list(posiciones_y), aceleracion_centripeta, tiempo_total_simulacion, estados_simulacion

def simular_movimiento_circular_uniforme(radio: float, velocidad_angular: float = None, velocidad_tangencial: float = None, tiempo_total_simulacion: float = None, num_puntos: int = 100):
    """
    Función para simular el Movimiento Circular Uniforme, diseñada para ser llamada desde una API.
    Retorna un diccionario con los resultados de la simulación.
    """
    try:
        tiempos, angulos_rad, posiciones_x, posiciones_y, aceleracion_centripeta, tiempo_total, estados = calcular_movimiento_circular_uniforme(
            radio, velocidad_angular, velocidad_tangencial, tiempo_total_simulacion, num_puntos
        )
        return {
            "parametros_entrada": {
                "radio": radio,
                "velocidad_angular": velocidad_angular,
                "velocidad_tangencial": velocidad_tangencial,
                "tiempo_total_simulacion": tiempo_total_simulacion,
                "num_puntos": num_puntos,
            },
            "resultados": {
                "tiempos": tiempos,
                "angulos_rad": angulos_rad,
                "posiciones_x": posiciones_x,
                "posiciones_y": posiciones_y,
                "aceleracion_centripeta": aceleracion_centripeta,
                "tiempo_total_simulacion": tiempo_total,
                "estados_simulacion": estados, # Matriz de estados [tiempo, angulo, pos_x, pos_y]
            },
            "mensaje": "Simulación de Movimiento Circular Uniforme calculada exitosamente."
        }
    except ValueError as e:
        return {"error": str(e), "mensaje": "Error en los parámetros de entrada."}
    except Exception as e:
        return {"error": str(e), "mensaje": "Ocurrió un error inesperado durante la simulación."}
