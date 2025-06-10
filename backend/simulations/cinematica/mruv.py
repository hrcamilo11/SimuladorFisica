import numpy as np

def calcular_mruv(posicion_inicial, velocidad_inicial, aceleracion, tiempo_total, num_puntos=100):
    """
    Calcula la posición y velocidad de un objeto en Movimiento Rectilíneo Uniformemente Variado (MRUV).
    x(t) = x0 + v0*t + 0.5*a*t^2
    v(t) = v0 + a*t
    """
    if tiempo_total < 0:
        raise ValueError("El tiempo total no puede ser negativo.")
    if num_puntos <= 1 and tiempo_total > 0:
        num_puntos = 2
    elif num_puntos < 1:
        num_puntos = 1

    tiempos = np.linspace(0, tiempo_total, num_puntos)
    posiciones = posicion_inicial + velocidad_inicial * tiempos + 0.5 * aceleracion * tiempos**2
    velocidades = velocidad_inicial + aceleracion * tiempos
    # Combinar los estados en una matriz para facilitar la animación
    estados_simulacion = np.array([tiempos, posiciones, velocidades]).T.tolist()

    return list(tiempos), list(posiciones), list(velocidades), estados_simulacion

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
