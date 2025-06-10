import numpy as np

def calcular_colision_elastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy, nx, ny):
    """
    Calcula las velocidades finales de dos partículas después de una colisión elástica 2D.
    Se requiere la normal de colisión (nx, ny) como un vector unitario.
    nx, ny: componentes del vector unitario normal a la superficie de contacto,
            apuntando desde la partícula 1 hacia la partícula 2 si chocan directamente,
            o a lo largo de la línea de acción de la fuerza de colisión.
    Retorna v1fx_f, v1fy_f, v2fx_f, v2fy_f, estados_simulacion.
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")
    
    norm_n = np.sqrt(nx**2 + ny**2)
    if not np.isclose(norm_n, 1.0):
        if norm_n == 0: raise ValueError("El vector normal de colisión no puede ser (0,0).")
        nx /= norm_n
        ny /= norm_n

    # Vector tangente unitario (tx, ty)
    tx = -ny
    ty = nx

    # Velocidades iniciales (vectores)
    v1_i = np.array([v1ix, v1iy])
    v2_i = np.array([v2ix, v2iy])

    # Componentes normales de las velocidades iniciales (escalares)
    v1n_i = v1_i[0] * nx + v1_i[1] * ny  # dot(v1_i, n_vec)
    v2n_i = v2_i[0] * nx + v2_i[1] * ny  # dot(v2_i, n_vec)

    # Componentes tangenciales de las velocidades iniciales (escalares)
    v1t_i = v1_i[0] * tx + v1_i[1] * ty  # dot(v1_i, t_vec)
    v2t_i = v2_i[0] * tx + v2_i[1] * ty  # dot(v2_i, t_vec)

    # Las componentes tangenciales no cambian en una colisión elástica sin fricción
    v1t_f = v1t_i
    v2t_f = v2t_i

    # Las componentes normales cambian según las fórmulas de colisión 1D
    v1n_f = (v1n_i * (m1 - m2) + 2 * m2 * v2n_i) / (m1 + m2)
    v2n_f = (v2n_i * (m2 - m1) + 2 * m1 * v1n_i) / (m1 + m2)

    # Recomponer las velocidades finales vectoriales
    v1fx_f = v1n_f * nx + v1t_f * tx
    v1fy_f = v1n_f * ny + v1t_f * ty
    
    v2fx_f = v2n_f * nx + v2t_f * tx
    v2fy_f = v2n_f * ny + v2t_f * ty

    # Para colisiones, el concepto de "tiempo de simulación" es instantáneo.
    # Creamos una matriz de estados para la animación.
    # Representaremos el estado inicial y el estado final.
    # Cada fila: [tiempo, posicion_x_obj1, posicion_y_obj1, velocidad_x_obj1, velocidad_y_obj1, posicion_x_obj2, posicion_y_obj2, velocidad_x_obj2, velocidad_y_obj2]
    # Asumimos posiciones iniciales arbitrarias para visualización.
    estados_simulacion = [
        [0, -1.0, 0, v1ix, v1iy, 1.0, 0, v2ix, v2iy], # Estado inicial
        [0, -1.0, 0, v1fx_f, v1fy_f, 1.0, 0, v2fx_f, v2fy_f]    # Estado final
    ]

    return v1fx_f, v1fy_f, v2fx_f, v2fy_f, estados_simulacion

def simular_colision_elastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy, nx, ny):
    """
    Función para simular una colisión elástica 2D, diseñada como un endpoint de API.
    """
    try:
        v1fx_f, v1fy_f, v2fx_f, v2fy_f, estados_simulacion = calcular_colision_elastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy, nx, ny)
        
        return {
            "success": True,
            "message": "Cálculo de colisión elástica 2D exitoso.",
            "parametros_entrada": {
                "m1": m1,
                "v1ix": v1ix,
                "v1iy": v1iy,
                "m2": m2,
                "v2ix": v2ix,
                "v2iy": v2iy,
                "nx": nx,
                "ny": ny
            },
            "resultados": {
                "v1fx_final": v1fx_f,
                "v1fy_final": v1fy_f,
                "v2fx_final": v2fx_f,
                "v2fy_final": v2fy_f
            },
            "estados_simulacion": estados_simulacion
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "parametros_entrada": {
                "m1": m1,
                "v1ix": v1ix,
                "v1iy": v1iy,
                "m2": m2,
                "v2ix": v2ix,
                "v2iy": v2iy,
                "nx": nx,
                "ny": ny
            },
            "resultados": None,
            "estados_simulacion": []
        }
