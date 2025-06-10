def calcular_longitud_onda(velocidad, frecuencia):
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
    estado_animacion = {"velocidad": velocidad, "frecuencia": frecuencia, "longitud_onda": longitud}
    return {"longitud_onda": longitud, "estado_animacion": estado_animacion}

def simular_longitud_onda(velocidad, frecuencia):
    """
    Función API para simular el cálculo de la longitud de onda.
    """
    try:
        resultados = calcular_longitud_onda(velocidad, frecuencia)
        return {
            "success": True,
            "message": "Cálculo de longitud de onda exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_frecuencia_onda(velocidad, longitud_onda):
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
    estado_animacion = {"velocidad": velocidad, "longitud_onda": longitud_onda, "frecuencia_onda": frecuencia_onda}
    return {"frecuencia_onda": frecuencia_onda, "estado_animacion": estado_animacion}

def simular_frecuencia_onda(velocidad, longitud_onda):
    """
    Función API para simular el cálculo de la frecuencia de onda.
    """
    try:
        resultados = calcular_frecuencia_onda(velocidad, longitud_onda)
        return {
            "success": True,
            "message": "Cálculo de frecuencia de onda exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_velocidad_onda(longitud_onda, frecuencia):
    """
    Calcula la velocidad (v) de una onda dada su longitud de onda (λ) y frecuencia (f).

    Args:
        longitud_onda (float): La longitud de onda en metros (m).
        frecuencia (float): La frecuencia de la onda en hercios (Hz).

    Returns:
        float: La velocidad de la onda en metros por segundo (m/s).
    """
    velocidad_onda = longitud_onda * frecuencia
    estado_animacion = {"longitud_onda": longitud_onda, "frecuencia": frecuencia, "velocidad_onda": velocidad_onda}
    return {"velocidad_onda": velocidad_onda, "estado_animacion": estado_animacion}

def simular_velocidad_onda(longitud_onda, frecuencia):
    """
    Función API para simular el cálculo de la velocidad de onda.
    """
    try:
        resultados = calcular_velocidad_onda(longitud_onda, frecuencia)
        return {
            "success": True,
            "message": "Cálculo de velocidad de onda exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }