import math

def calcular_frecuencia_observada_doppler(frecuencia_fuente: float, velocidad_onda: float, velocidad_observador: float, velocidad_fuente: float, direccion_observador: str, direccion_fuente: str) -> float:
    """
    Calcula la frecuencia observada debido al efecto Doppler.

    Args:
        frecuencia_fuente (float): Frecuencia de la fuente en Hz.
        velocidad_onda (float): Velocidad de la onda (ej. velocidad del sonido en el aire) en m/s.
        velocidad_observador (float): Velocidad del observador en m/s.
        velocidad_fuente (float): Velocidad de la fuente en m/s.
        direccion_observador (str): 'acercandose' o 'alejandose' del observador respecto a la fuente.
        direccion_fuente (str): 'acercandose' o 'alejandose' de la fuente respecto al observador.

    Returns:
        float: Frecuencia observada en Hz.

    Raises:
        ValueError: Si la velocidad de la onda es cero.
    """
    if velocidad_onda == 0:
        raise ValueError("La velocidad de la onda no puede ser cero.")

    v_o = velocidad_observador
    v_s = velocidad_fuente

    if direccion_observador == 'acercandose':
        v_o = -v_o
    elif direccion_observador == 'alejandose':
        v_o = v_o
    else:
        raise ValueError("Dirección del observador no válida. Use 'acercandose' o 'alejandose'.")

    if direccion_fuente == 'acercandose':
        v_s = -v_s
    elif direccion_fuente == 'alejandose':
        v_s = v_s
    else:
        raise ValueError("Dirección de la fuente no válida. Use 'acercandose' o 'alejandose'.")

    frecuencia_observada = frecuencia_fuente * ((velocidad_onda + v_o) / (velocidad_onda + v_s))
    return frecuencia_observada

def calcular_intensidad_sonido(potencia_fuente: float, distancia: float) -> float:
    """
    Calcula la intensidad del sonido (I) a una distancia dada de una fuente puntual.

    Args:
        potencia_fuente (float): La potencia de la fuente de sonido en vatios (W).
        distancia (float): La distancia desde la fuente en metros (m).

    Returns:
        float: La intensidad del sonido en vatios por metro cuadrado (W/m²).

    Raises:
        ValueError: Si la distancia es cero.
    """
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    intensidad = potencia_fuente / (4 * math.pi * (distancia**2))
    return intensidad

def calcular_nivel_intensidad_sonido(intensidad: float, intensidad_referencia: float = 1e-12) -> float:
    """
    Calcula el nivel de intensidad del sonido (β) en decibelios (dB).

    Args:
        intensidad (float): La intensidad del sonido en vatios por metro cuadrado (W/m²).
        intensidad_referencia (float): La intensidad de referencia (umbral de audición) en W/m².

    Returns:
        float: El nivel de intensidad del sonido en decibelios (dB).

    Raises:
        ValueError: Si la intensidad o la intensidad de referencia son cero o negativas.
    """
    if intensidad <= 0 or intensidad_referencia <= 0:
        raise ValueError("La intensidad y la intensidad de referencia deben ser mayores que cero.")
    nivel_intensidad = 10 * math.log10(intensidad / intensidad_referencia)
    return nivel_intensidad

def calcular_longitud_onda(velocidad: float, frecuencia: float) -> float:
    """
    Calcula la longitud de onda (λ) dada la velocidad (v) y la frecuencia (f).

    Args:
        velocidad (float): La velocidad de la onda en metros por segundo (m/s).
        frecuencia (float): La frecuencia de la onda en hercios (Hz).

    Returns:
        float: La longitud de onda en metros (m).

    Raises:
        ValueError: Si la frecuencia es cero.
    """
    if frecuencia == 0:
        raise ValueError("La frecuencia no puede ser cero.")
    longitud = velocidad / frecuencia
    return longitud

def calcular_frecuencia_onda(velocidad: float, longitud_onda: float) -> float:
    """
    Calcula la frecuencia (f) dada la velocidad (v) y la longitud de onda (λ).

    Args:
        velocidad (float): La velocidad de la onda en metros por segundo (m/s).
        longitud_onda (float): La longitud de onda en metros (m).

    Returns:
        float: La frecuencia de la onda en hercios (Hz).

    Raises:
        ValueError: Si la longitud de onda es cero.
    """
    if longitud_onda == 0:
        raise ValueError("La longitud de onda no puede ser cero.")
    frecuencia_onda = velocidad / longitud_onda
    return frecuencia_onda

def calcular_velocidad_onda(longitud_onda: float, frecuencia: float) -> float:
    """
    Calcula la velocidad (v) de una onda dada su longitud de onda (λ) y frecuencia (f).

    Args:
        longitud_onda (float): La longitud de onda en metros (m).
        frecuencia (float): La frecuencia de la onda en hercios (Hz).

    Returns:
        float: La velocidad de la onda en metros por segundo (m/s).
    """
    velocidad_onda = longitud_onda * frecuencia
    return velocidad_onda

def calcular_angulo_refraccion(angulo_incidencia_grados: float, indice_refraccion1: float, indice_refraccion2: float) -> float:
    """
    Calcula el ángulo de refracción utilizando la Ley de Snell.

    Args:
        angulo_incidencia_grados (float): El ángulo de incidencia en grados.
        indice_refraccion1 (float): El índice de refracción del primer medio.
        indice_refraccion2 (float): El índice de refracción del segundo medio.

    Returns:
        float: El ángulo de refracción en grados.

    Raises:
        ValueError: Si el índice de refracción del segundo medio es cero.
    """
    if indice_refraccion2 == 0:
        raise ValueError("El índice de refracción del segundo medio no puede ser cero.")

    angulo_incidencia_radianes = math.radians(angulo_incidencia_grados)
    sin_angulo_refraccion = (indice_refraccion1 * math.sin(angulo_incidencia_radianes)) / indice_refraccion2

    if abs(sin_angulo_refraccion) > 1:
        raise ValueError("No hay ángulo de refracción real (reflexión total interna).")

    angulo_refraccion_radianes = math.asin(sin_angulo_refraccion)
    angulo_refraccion_grados = math.degrees(angulo_refraccion_radianes)
    return angulo_refraccion_grados

def calcular_velocidad_onda_medio(velocidad_luz_vacio: float, indice_refraccion: float) -> float:
    """
    Calcula la velocidad de una onda en un medio dado su índice de refracción.

    Args:
        velocidad_luz_vacio (float): La velocidad de la luz en el vacío en m/s.
        indice_refraccion (float): El índice de refracción del medio.

    Returns:
        float: La velocidad de la onda en el medio en m/s.

    Raises:
        ValueError: Si el índice de refracción es cero.
    """
    if indice_refraccion == 0:
        raise ValueError("El índice de refracción no puede ser cero.")
    velocidad_onda = velocidad_luz_vacio / indice_refraccion
    return velocidad_onda