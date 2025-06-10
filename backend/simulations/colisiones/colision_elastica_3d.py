import numpy as np

def calcular_colision_elastica_3d(m1, v1i, m2, v2i, n_vec):
    """
    Calcula las velocidades finales de dos partículas después de una colisión elástica 3D.
    v1i, v2i: tuplas o listas de 3 elementos (vx, vy, vz) para las velocidades iniciales.
    n_vec: tupla o lista de 3 elementos (nx, ny, nz) para el vector normal de colisión unitario.
    Retorna (v1fx, v1fy, v1fz), (v2fx, v2fy, v2fz), estados_simulacion.
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")

    v1i_arr = np.array(v1i)
    v2i_arr = np.array(v2i)
    n_arr = np.array(n_vec)

    norm_n = np.linalg.norm(n_arr)
    if not np.isclose(norm_n, 1.0):
        if np.isclose(norm_n, 0.0): 
            raise ValueError("El vector normal de colisión no puede ser (0,0,0).")
        n_arr = n_arr / norm_n # Normalizar

    # Componentes escalares de las velocidades iniciales a lo largo de la normal n
    v1n_i_scalar = np.dot(v1i_arr, n_arr)
    v2n_i_scalar = np.dot(v2i_arr, n_arr)

    # Componentes vectoriales tangenciales de las velocidades iniciales
    v1t_i_vec = v1i_arr - v1n_i_scalar * n_arr
    v2t_i_vec = v2i_arr - v2n_i_scalar * n_arr

    # Las componentes tangenciales (vectoriales) no cambian
    v1t_f_vec = v1t_i_vec
    v2t_f_vec = v2t_i_vec

    # Las componentes normales (escalares) cambian según las fórmulas de colisión 1D
    v1n_f_scalar = (v1n_i_scalar * (m1 - m2) + 2 * m2 * v2n_i_scalar) / (m1 + m2)
    v2n_f_scalar = (v2n_i_scalar * (m2 - m1) + 2 * m1 * v1n_i_scalar) / (m1 + m2)

    # Componentes vectoriales normales finales
    v1n_f_vec = v1n_f_scalar * n_arr
    v2n_f_vec = v2n_f_scalar * n_arr

    # Recomponer las velocidades finales vectoriales
    v1f_arr = v1n_f_vec + v1t_f_vec
    v2f_arr = v2n_f_vec + v2t_f_vec

    # Para colisiones, el concepto de "tiempo de simulación" es instantáneo.
    # Creamos una matriz de estados para la animación.
    # Cada fila: [tiempo, posicion_x_obj1, posicion_y_obj1, posicion_z_obj1, velocidad_x_obj1, velocidad_y_obj1, velocidad_z_obj1, posicion_x_obj2, posicion_y_obj2, posicion_z_obj2, velocidad_x_obj2, velocidad_y_obj2, velocidad_z_obj2]
    # Asumimos posiciones iniciales arbitrarias para visualización.
    estados_simulacion = [
        [0, -1.0, 0, 0, v1i[0], v1i[1], v1i[2], 1.0, 0, 0, v2i[0], v2i[1], v2i[2]], # Estado inicial
        [0, -1.0, 0, 0, v1f_arr[0], v1f_arr[1], v1f_arr[2], 1.0, 0, 0, v2f_arr[0], v2f_arr[1], v2f_arr[2]]    # Estado final
    ]

    return tuple(v1f_arr), tuple(v2f_arr), estados_simulacion

def simular_colision_elastica_3d(m1, v1i, m2, v2i, n_vec):
    """
    Función para simular una colisión elástica 3D, diseñada como un endpoint de API.
    """
    try:
        v1f, v2f, estados_simulacion = calcular_colision_elastica_3d(m1, v1i, m2, v2i, n_vec)
        
        return {
            "success": True,
            "message": "Cálculo de colisión elástica 3D exitoso.",
            "parametros_entrada": {
                "m1": m1,
                "v1i": v1i,
                "m2": m2,
                "v2i": v2i,
                "n_vec": n_vec
            },
            "resultados": {
                "v1_final": v1f,
                "v2_final": v2f
            },
            "estados_simulacion": estados_simulacion
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "parametros_entrada": {
                "m1": m1,
                "v1i": v1i,
                "m2": m2,
                "v2i": v2i,
                "n_vec": n_vec
            },
            "resultados": None,
            "estados_simulacion": []
        }
