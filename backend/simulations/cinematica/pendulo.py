import numpy as np

from backend.Ecuaciones.cinematica.pendulo import calcular_pendulo_simple

def simular_pendulo_simple(longitud: float, angulo_inicial_grados: float, tiempo_total_simulacion: float = None, num_puntos: int = 200):
    """
    Función para simular el péndulo simple, diseñada para ser llamada desde una API.
    Retorna un diccionario con los resultados de la simulación.
    """
    try:
        angulo_inicial_rad = np.deg2rad(angulo_inicial_grados)
        tiempos, angulos_rad, velocidades_angulares, aceleraciones_angulares, pos_x, pos_y, periodo, frecuencia_angular, estados = calcular_pendulo_simple(
            longitud, angulo_inicial_rad, tiempo_total_simulacion=tiempo_total_simulacion, num_puntos=num_puntos
        )
        return {
            "parametros_entrada": {
                "longitud": longitud,
                "angulo_inicial_grados": angulo_inicial_grados,
                "tiempo_total_simulacion": tiempo_total_simulacion,
                "num_puntos": num_puntos,
            },
            "resultados": {
                "tiempos": tiempos,
                "angulos_rad": angulos_rad,
                "velocidades_angulares": velocidades_angulares,
                "aceleraciones_angulares": aceleraciones_angulares,
                "posiciones_x": pos_x,
                "posiciones_y": pos_y,
                "periodo": periodo,
                "frecuencia_angular": frecuencia_angular,
                "estados_simulacion": estados, # Matriz de estados [tiempo, angulo_rad, vel_angular, acel_angular, pos_x, pos_y]
            },
            "mensaje": "Simulación de péndulo simple calculada exitosamente."
        }
    except ValueError as e:
        return {"error": str(e), "mensaje": "Error en los parámetros de entrada."}
    except Exception as e:
        return {"error": str(e), "mensaje": "Ocurrió un error inesperado durante la simulación."}
