import numpy as np
from backend.Ecuaciones.cinematica.caida_libre import calcular_caida_libre

GRAVEDAD = 9.81  # m/s^2

def simular_caida_libre(altura_inicial: float, tiempo_total_simulacion: float = None, num_puntos: int = 100):
    """
    Función para simular la caída libre, diseñada para ser llamada desde una API.
    Retorna un diccionario con los resultados de la simulación.
    """
    try:
        tiempos, alturas, velocidades, tiempo_total, estados = calcular_caida_libre(
            altura_inicial, tiempo_total_simulacion, num_puntos
        )
        return {
            "parametros_entrada": {
                "altura_inicial": altura_inicial,
                "tiempo_total_simulacion": tiempo_total_simulacion,
                "num_puntos": num_puntos,
            },
            "resultados": {
                "tiempos": tiempos,
                "alturas": alturas,
                "velocidades": velocidades,
                "tiempo_total_simulacion": tiempo_total,
                "estados_simulacion": estados, # Matriz de estados [tiempo, altura, velocidad]
            },
            "mensaje": "Simulación de caída libre calculada exitosamente."
        }
    except ValueError as e:
        return {"error": str(e), "mensaje": "Error en los parámetros de entrada."}
    except Exception as e:
        return {"error": str(e), "mensaje": "Ocurrió un error inesperado durante la simulación."}
