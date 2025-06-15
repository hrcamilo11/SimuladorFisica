from backend.Ecuaciones.cinematica.tiro_parabolico import calcular_tiro_parabolico

def simular_tiro_parabolico(velocidad_inicial: float, angulo_lanzamiento_grados: float, altura_inicial: float = 0, num_puntos: int = 100):
    """
    Función para simular el tiro parabólico, diseñada para ser llamada desde una API.
    Retorna un diccionario con los resultados de la simulación.
    """
    try:
        tiempos, posiciones_x, posiciones_y, tiempo_total, estados = calcular_tiro_parabolico(
            velocidad_inicial, angulo_lanzamiento_grados, altura_inicial, num_puntos
        )
        return {
            "parametros_entrada": {
                "velocidad_inicial": velocidad_inicial,
                "angulo_lanzamiento_grados": angulo_lanzamiento_grados,
                "altura_inicial": altura_inicial,
                "num_puntos": num_puntos,
            },
            "resultados": {
                "tiempos": tiempos,
                "posiciones_x": posiciones_x,
                "posiciones_y": posiciones_y,
                "tiempo_total_simulacion": tiempo_total,
                "estados_simulacion": estados, # Matriz de estados [tiempo, pos_x, pos_y]
            },
            "mensaje": "Simulación de tiro parabólico calculada exitosamente."
        }
    except ValueError as e:
        return {"error": str(e), "mensaje": "Error en los parámetros de entrada."}
    except Exception as e:
        return {"error": str(e), "mensaje": "Ocurrió un error inesperado durante la simulación."}
