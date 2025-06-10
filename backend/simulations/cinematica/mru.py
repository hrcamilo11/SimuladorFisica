import numpy as np

def calcular_mru(posicion_inicial, velocidad, tiempo_total, num_puntos=100):
    """
    Calcula la posición de un objeto en Movimiento Rectilíneo Uniforme (MRU).
    x(t) = x0 + v*t
    """
    if tiempo_total < 0:
        raise ValueError("El tiempo total no puede ser negativo.")
    if num_puntos <= 1 and tiempo_total > 0:
        # Need at least 2 points to form a line for positive time
        num_puntos = 2 
    elif num_puntos < 1:
        num_puntos = 1 # Single point if time is zero or for safety

    tiempos = np.linspace(0, tiempo_total, num_puntos)
    posiciones = posicion_inicial + velocidad * tiempos
    # Combinar los estados en una matriz para facilitar la animación
    estados_simulacion = np.array([tiempos, posiciones]).T.tolist()

    return list(tiempos), list(posiciones), estados_simulacion

def simular_mru(posicion_inicial: float, velocidad: float, tiempo_total: float, num_puntos: int = 100):
    """
    Función para simular el Movimiento Rectilíneo Uniforme (MRU), diseñada para ser llamada desde una API.
    Retorna un diccionario con los resultados de la simulación.
    """
    try:
        tiempos, posiciones, estados = calcular_mru(
            posicion_inicial, velocidad, tiempo_total, num_puntos
        )
        return {
            "parametros_entrada": {
                "posicion_inicial": posicion_inicial,
                "velocidad": velocidad,
                "tiempo_total": tiempo_total,
                "num_puntos": num_puntos,
            },
            "resultados": {
                "tiempos": tiempos,
                "posiciones": posiciones,
                "estados_simulacion": estados, # Matriz de estados [tiempo, posicion]
            },
            "mensaje": "Simulación de MRU calculada exitosamente."
        }
    except ValueError as e:
        return {"error": str(e), "mensaje": "Error en los parámetros de entrada."}
    except Exception as e:
        return {"error": str(e), "mensaje": "Ocurrió un error inesperado durante la simulación."}
