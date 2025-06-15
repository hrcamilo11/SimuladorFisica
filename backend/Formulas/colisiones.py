import numpy as np

def calcular_coeficiente_restitucion(v1_inicial: float, v2_inicial: float, v1_final: float, v2_final: float) -> float:
    """
    Calcula el coeficiente de restitución (e) para una colisión 1D.

    Args:
        v1_inicial (float): Velocidad inicial del objeto 1.
        v2_inicial (float): Velocidad inicial del objeto 2.
        v1_final (float): Velocidad final del objeto 1.
        v2_final (float): Velocidad final del objeto 2.

    Returns:
        float: El coeficiente de restitución (e).

    Raises:
        ValueError: Si la diferencia de velocidades iniciales es cero, lo que resultaría en una división por cero.
    """
    denominador = v1_inicial - v2_inicial
    if denominador == 0:
        raise ValueError("La diferencia de velocidades iniciales no puede ser cero para calcular el coeficiente de restitución.")
    
    e = -(v1_final - v2_final) / denominador
    return e

def calcular_velocidades_finales_colision_elastica_1d(m1: float, v1_inicial: float, m2: float, v2_inicial: float) -> tuple[float, float]:
    """
    Calcula las velocidades finales de dos objetos después de una colisión elástica 1D.

    Args:
        m1 (float): Masa del objeto 1.
        v1_inicial (float): Velocidad inicial del objeto 1.
        m2 (float): Masa del objeto 2.
        v2_inicial (float): Velocidad inicial del objeto 2.

    Returns:
        tuple[float, float]: Una tupla que contiene (v1_final, v2_final).

    Raises:
        ValueError: Si alguna de las masas es no positiva.
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")

    v1_final = ((m1 - m2) / (m1 + m2)) * v1_inicial + ((2 * m2) / (m1 + m2)) * v2_inicial
    v2_final = ((2 * m1) / (m1 + m2)) * v1_inicial + ((m2 - m1) / (m1 + m2)) * v2_inicial

    return v1_final, v2_final

def calcular_velocidades_finales_colision_elastica_2d(m1: float, v1ix: float, v1iy: float, m2: float, v2ix: float, v2iy: float, nx: float, ny: float) -> tuple[float, float, float, float]:
    """
    Calcula las velocidades finales de dos partículas después de una colisión elástica 2D.

    Args:
        m1 (float): Masa del objeto 1.
        v1ix (float): Componente x de la velocidad inicial del objeto 1.
        v1iy (float): Componente y de la velocidad inicial del objeto 1.
        m2 (float): Masa del objeto 2.
        v2ix (float): Componente x de la velocidad inicial del objeto 2.
        v2iy (float): Componente y de la velocidad inicial del objeto 2.
        nx (float): Componente x del vector unitario normal a la superficie de contacto.
        ny (float): Componente y del vector unitario normal a la superficie de contacto.

    Returns:
        tuple[float, float, float, float]: Una tupla que contiene (v1fx_final, v1fy_final, v2fx_final, v2fy_final).

    Raises:
        ValueError: Si alguna de las masas es no positiva o el vector normal es cero.
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

    return v1fx_f, v1fy_f, v2fx_f, v2fy_f

def calcular_velocidades_finales_colision_elastica_3d(m1: float, v1i: list[float], m2: float, v2i: list[float], n_vec: list[float]) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """
    Calcula las velocidades finales de dos partículas después de una colisión elástica 3D.

    Args:
        m1 (float): Masa del objeto 1.
        v1i (list[float]): Velocidad inicial del objeto 1 como [vx, vy, vz].
        m2 (float): Masa del objeto 2.
        v2i (list[float]): Velocidad inicial del objeto 2 como [vx, vy, vz].
        n_vec (list[float]): Vector normal de colisión unitario como [nx, ny, nz].

    Returns:
        tuple[tuple[float, float, float], tuple[float, float, float]]: Una tupla que contiene las velocidades finales de ambos objetos ((v1fx, v1fy, v1fz), (v2fx, v2fy, v2fz)).

    Raises:
        ValueError: Si alguna de las masas es no positiva o el vector normal es cero.
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

    return tuple(v1f_arr), tuple(v2f_arr)

def calcular_velocidad_final_colision_perfectamente_inelastica_1d(m1, v1_inicial, m2, v2_inicial):
    """
    Calcula la velocidad final común de dos objetos después de una colisión perfectamente inelástica 1D.
    Los objetos quedan unidos después del choque.
    m1, m2: masas de los objetos.
    v1_inicial, v2_inicial: velocidades iniciales de los objetos.
    Retorna v_final_comun.
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")

    # Conservación del momento lineal: m1*v1_i + m2*v2_i = (m1 + m2)*v_f_comun
    v_final_comun = (m1 * v1_inicial + m2 * v2_inicial) / (m1 + m2)
    
    return v_final_comun

def calcular_velocidad_final_colision_perfectamente_inelastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy):
    """
    Calcula la velocidad final común de dos partículas después de una colisión perfectamente inelástica 2D.
    Retorna vfx, vfy.
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

    return vfx, vfy

def calcular_impulso(fuerza: float, tiempo: float) -> float:
    """
    Calcula el impulso (J) dado una fuerza constante y un intervalo de tiempo.

    Args:
        fuerza (float): La fuerza aplicada (N).
        tiempo (float): El intervalo de tiempo durante el cual se aplica la fuerza (s).

    Returns:
        float: El impulso (N·s).

    Raises:
        ValueError: Si el tiempo es negativo.
    """
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    return fuerza * tiempo

def calcular_cambio_momento_lineal(masa: float, velocidad_inicial: float, velocidad_final: float) -> float:
    """
    Calcula el cambio en el momento lineal (Δp) de un objeto.

    Args:
        masa (float): La masa del objeto (kg).
        velocidad_inicial (float): La velocidad inicial del objeto (m/s).
        velocidad_final (float): La velocidad final del objeto (m/s).

    Returns:
        float: El cambio en el momento lineal (kg·m/s).

    Raises:
        ValueError: Si la masa es no positiva.
    """
    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")
    return masa * (velocidad_final - velocidad_inicial)

def calcular_momento_lineal(masa: float, velocidad: float) -> float:
    """
    Calcula el momento lineal (p) de un objeto.

    Args:
        masa (float): La masa del objeto (kg).
        velocidad (float): La velocidad del objeto (m/s).

    Returns:
        float: El momento lineal (kg·m/s).

    Raises:
        ValueError: Si la masa es no positiva.
    """
    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")
    return masa * velocidad