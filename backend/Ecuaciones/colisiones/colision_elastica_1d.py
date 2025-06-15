import numpy as np

def calcular_colision_elastica_1d(m1, v1_inicial, m2, v2_inicial):
    """
    Calcula las velocidades finales de dos objetos después de una colisión elástica 1D.
    m1, m2: masas de los objetos.
    v1_inicial, v2_inicial: velocidades iniciales de los objetos.
    Retorna v1_final, v2_final, estados_simulacion.
    """
    if m1 <= 0 or m2 <= 0:
        # Masas deben ser positivas
        # Para la simulación, si las masas no son válidas, no hay colisión significativa.
        # Podríamos retornar un error o las velocidades iniciales y un estado vacío.
        raise ValueError("Las masas deben ser positivas.")

    # Conservación del momento lineal y energía cinética para colisión elástica:
    v1_final = ((m1 - m2) / (m1 + m2)) * v1_inicial + ((2 * m2) / (m1 + m2)) * v2_inicial
    v2_final = ((2 * m1) / (m1 + m2)) * v1_inicial + ((m2 - m1) / (m1 + m2)) * v2_inicial
    
    # Para colisiones, el concepto de "tiempo de simulación" es instantáneo.
    # Creamos una matriz de estados para la animación.
    # Representaremos el estado inicial y el estado final.
    # Cada fila: [tiempo, posicion_x_obj1, posicion_y_obj1, velocidad_x_obj1, velocidad_y_obj1, posicion_x_obj2, posicion_y_obj2, velocidad_x_obj2, velocidad_y_obj2]
    # En 1D, y-componentes y posiciones son 0 o irrelevantes para el cálculo, pero se incluyen para consistencia con 2D/3D.
    # Asumimos que la colisión ocurre en x=0 para simplificar la visualización.
    estados_simulacion = [
        [0, -1.0, 0, v1_inicial, 0, 1.0, 0, v2_inicial, 0], # Estado inicial (posiciones arbitrarias para visualización)
        [0, -1.0, 0, v1_final, 0, 1.0, 0, v2_final, 0]    # Estado final (mismo tiempo, nuevas velocidades)
    ]

    return v1_final, v2_final, estados_simulacion