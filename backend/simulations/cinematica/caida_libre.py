import numpy as np

GRAVEDAD = 9.81  # m/s^2

def calcular_caida_libre(altura_inicial, tiempo_total_simulacion=None, num_puntos=100):
    """
    Calcula la posición y velocidad de un objeto en caída libre.
    Si tiempo_total_simulacion no se provee, se calcula hasta que toque el suelo.
    Retorna tiempos, alturas y velocidades.
    """
    if altura_inicial <= 0:
        return [], [], []

    if tiempo_total_simulacion is None:
        # Tiempo para alcanzar el suelo: h = 0.5 * g * t^2 => t = sqrt(2h/g)
        tiempo_hasta_suelo = np.sqrt(2 * altura_inicial / GRAVEDAD)
        tiempo_total_simulacion = tiempo_hasta_suelo

    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    alturas = altura_inicial - 0.5 * GRAVEDAD * tiempos**2
    velocidades = -GRAVEDAD * tiempos # Negativo indica hacia abajo

    # Asegurarse de que la altura no sea negativa y el tiempo no exceda el impacto
    alturas_reales = []
    velocidades_reales = []
    tiempos_reales = []

    for t, h, v in zip(tiempos, alturas, velocidades):
        if h >= 0:
            alturas_reales.append(h)
            velocidades_reales.append(v)
            tiempos_reales.append(t)
        else:
            # Interpolar para encontrar el tiempo exacto de impacto si es necesario
            if not alturas_reales or alturas_reales[-1] > 0: # Solo si no hemos añadido ya el punto de impacto
                # Tiempo para h=0 desde el último punto positivo
                # h_prev - 0.5 * g * (t_impact - t_prev)^2 = 0 ... es más complejo
                # Simplificación: añadir el punto de impacto
                tiempo_impacto_real = np.sqrt(2 * altura_inicial / GRAVEDAD)
                if tiempo_impacto_real > (tiempos_reales[-1] if tiempos_reales else 0):
                     alturas_reales.append(0)
                     velocidades_reales.append(-GRAVEDAD * tiempo_impacto_real)
                     tiempos_reales.append(tiempo_impacto_real)
            break # Detener después del impacto
            
    # Combinar los estados en una matriz para facilitar la animación
    estados_simulacion = np.array([tiempos_reales, alturas_reales, velocidades_reales]).T.tolist()

    return tiempos_reales, alturas_reales, velocidades_reales, tiempo_total_simulacion, estados_simulacion

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
