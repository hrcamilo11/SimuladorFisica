import numpy as np

def calcular_colision_perfectamente_inelastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy):
    """
    Calcula la velocidad final común de dos partículas después de una colisión perfectamente inelástica 2D.
    Retorna vfx, vfy, estados_simulacion.
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")

    # Conservación del momento lineal en x
    px_total_inicial = m1 * v1ix + m2 * v2ix
    # Conservación del momento lineal en y
    py_total_inicial = m1 * v1iy + m2 * v2iy

    # Masa total después de la colisión
    m_total = m1 + m2

    # Velocidad final común (componentes x e y)
    vfx = px_total_inicial / m_total
    vfy = py_total_inicial / m_total

    # Para colisiones, el concepto de "tiempo de simulación" es instantáneo.
    # Creamos una matriz de estados para la animación.
    # Cada fila: [tiempo, posicion_x_obj1, posicion_y_obj1, velocidad_x_obj1, velocidad_y_obj1, posicion_x_obj2, posicion_y_obj2, velocidad_x_obj2, velocidad_y_obj2]
    # Asumimos posiciones iniciales arbitrarias para visualización.
    estados_simulacion = [
        [0, -1.0, 0, v1ix, v1iy, 1.0, 0, v2ix, v2iy], # Estado inicial
        [0, 0.0, 0, vfx, vfy, 0.0, 0, vfx, vfy]    # Estado final (objetos unidos en el origen)
    ]

    return vfx, vfy, estados_simulacion