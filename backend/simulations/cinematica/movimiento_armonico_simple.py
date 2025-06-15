import numpy as np

from backend.Ecuaciones.cinematica.movimiento_armonico_simple import calcular_movimiento_armonico_simple

def simular_movimiento_armonico_simple(amplitud: float, frecuencia_angular: float, fase_inicial: float, tiempo_total_simulacion: float, num_puntos: int = 100):
    """
    Función para simular el Movimiento Armónico Simple, diseñada para ser llamada desde una API.
    Retorna un diccionario con los resultados de la simulación.
    """
    try:
        tiempos, posiciones, velocidades, aceleraciones, periodo, frecuencia_hz, estados = calcular_movimiento_armonico_simple(
            amplitud, frecuencia_angular, fase_inicial, tiempo_total_simulacion, num_puntos
        )
        return {
            "parametros_entrada": {
                "amplitud": amplitud,
                "frecuencia_angular": frecuencia_angular,
                "fase_inicial": fase_inicial,
                "tiempo_total_simulacion": tiempo_total_simulacion,
                "num_puntos": num_puntos,
            },
            "resultados": {
                "tiempos": tiempos,
                "posiciones": posiciones,
                "velocidades": velocidades,
                "aceleraciones": aceleraciones,
                "periodo": periodo,
                "frecuencia_hz": frecuencia_hz,
                "estados_simulacion": estados, # Matriz de estados [tiempo, posicion, velocidad, aceleracion]
            },
            "mensaje": "Simulación de Movimiento Armónico Simple calculada exitosamente."
        }
    except ValueError as e:
        return {"error": str(e), "mensaje": "Error en los parámetros de entrada."}
    except Exception as e:
        return {"error": str(e), "mensaje": "Ocurrió un error inesperado durante la simulación."}
