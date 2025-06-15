import numpy as np

from backend.Ecuaciones.cinematica.movimiento_circular_uniforme import calcular_movimiento_circular_uniforme

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
