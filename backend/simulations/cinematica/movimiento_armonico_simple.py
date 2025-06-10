import numpy as np

def calcular_movimiento_armonico_simple(amplitud, frecuencia_angular, fase_inicial, tiempo_total_simulacion, num_puntos=100):
    """
    Calcula la posición, velocidad y aceleración de un objeto en Movimiento Armónico Simple.
    x(t) = A * cos(ω*t + φ)
    v(t) = -Aω * sin(ω*t + φ)
    a(t) = -Aω^2 * cos(ω*t + φ) = -ω^2 * x(t)
    """
    if amplitud <= 0:
        raise ValueError("La amplitud debe ser positiva.")
    if frecuencia_angular <= 0:
        raise ValueError("La frecuencia angular (ω) debe ser positiva.")
    if tiempo_total_simulacion <= 0:
        raise ValueError("El tiempo total de simulación debe ser positivo.")

    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    
    posiciones = amplitud * np.cos(frecuencia_angular * tiempos + fase_inicial)
    velocidades = -amplitud * frecuencia_angular * np.sin(frecuencia_angular * tiempos + fase_inicial)
    aceleraciones = -amplitud * (frecuencia_angular**2) * np.cos(frecuencia_angular * tiempos + fase_inicial)
    # Alternativamente: aceleraciones = -(frecuencia_angular**2) * posiciones

    periodo = 2 * np.pi / frecuencia_angular
    frecuencia_hz = 1 / periodo

    # Combinar los estados en una matriz para facilitar la animación
    estados_simulacion = np.array([tiempos, posiciones, velocidades, aceleraciones]).T.tolist()

    return list(tiempos), list(posiciones), list(velocidades), list(aceleraciones), periodo, frecuencia_hz, estados_simulacion

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
