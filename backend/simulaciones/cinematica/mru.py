import numpy as np
from backend.Ecuaciones.cinematica.ecuaciones_cinematicas import calcular_posicion_final_tiempo

from backend.Ecuaciones.cinematica.mru import calcular_mru

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
