import numpy as np
from backend.Ecuaciones.cinematica.ecuaciones_cinematicas import calcular_posicion_final_tiempo, calcular_velocidad_final_tiempo

from backend.Ecuaciones.cinematica.mruv import calcular_mruv

def simular_mruv(posicion_inicial: float, velocidad_inicial: float, aceleracion: float, tiempo_total: float, num_puntos: int = 100):
    """
    Función para simular el Movimiento Rectilíneo Uniformemente Variado (MRUV), diseñada para ser llamada desde una API.
    Retorna un diccionario con los resultados de la simulación.
    """
    try:
        tiempos, posiciones, velocidades, estados = calcular_mruv(
            posicion_inicial, velocidad_inicial, aceleracion, tiempo_total, num_puntos
        )
        return {
            "parametros_entrada": {
                "posicion_inicial": posicion_inicial,
                "velocidad_inicial": velocidad_inicial,
                "aceleracion": aceleracion,
                "tiempo_total": tiempo_total,
                "num_puntos": num_puntos,
            },
            "resultados": {
                "tiempos": tiempos,
                "posiciones": posiciones,
                "velocidades": velocidades,
                "estados_simulacion": estados, # Matriz de estados [tiempo, posicion, velocidad]
            },
            "mensaje": "Simulación de MRUV calculada exitosamente."
        }
    except ValueError as e:
        return {"error": str(e), "mensaje": "Error en los parámetros de entrada."}
    except Exception as e:
        return {"error": str(e), "mensaje": "Ocurrió un error inesperado durante la simulación."}
