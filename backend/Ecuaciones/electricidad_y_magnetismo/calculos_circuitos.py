def calcular_circuito_serie(resistencias):
    """
    Calcula la resistencia total de un circuito en serie.

    Args:
        resistencias (list): Una lista de resistencias en ohmios (Ω).

    Returns:
        dict: Un diccionario con la resistencia total y el estado para animación.
    """
    resistencia_total = sum(resistencias)
    estado_animacion = {"resistencias": resistencias, "resistencia_total": resistencia_total}
    return {"resistencia_total": resistencia_total, "estado_animacion": estado_animacion}

def calcular_circuito_paralelo(resistencias):
    """
    Calcula la resistencia total de un circuito en paralelo.

    Args:
        resistencias (list): Una lista de resistencias en ohmios (Ω).

    Returns:
        dict: Un diccionario con la resistencia total y el estado para animación.

    Raises:
        ValueError: Si alguna de las resistencias es cero.
    """
    if not resistencias:
        resistencia_total = 0.0
    else:
        for r in resistencias:
            if r == 0:
                raise ValueError("Las resistencias en paralelo no pueden ser cero.")
        resistencia_total = 1 / sum(1/r for r in resistencias)
    
    estado_animacion = {"resistencias": resistencias, "resistencia_total": resistencia_total}
    return {"resistencia_total": resistencia_total, "estado_animacion": estado_animacion}

def calcular_corriente_total(voltaje_total, resistencia_total):
    """
    Calcula la corriente total en un circuito.

    Args:
        voltaje_total (float): El voltaje total en voltios (V).
        resistencia_total (float): La resistencia total en ohmios (Ω).

    Returns:
        dict: Un diccionario con la corriente total y el estado para animación.

    Raises:
        ValueError: Si la resistencia total es cero.
    """
    if resistencia_total == 0:
        raise ValueError("La resistencia total no puede ser cero para calcular la corriente.")
    corriente_total = voltaje_total / resistencia_total
    estado_animacion = {"voltaje_total": voltaje_total, "resistencia_total": resistencia_total, "corriente_total": corriente_total}
    return {"corriente_total": corriente_total, "estado_animacion": estado_animacion}

def calcular_voltaje_paralelo(corriente_total, resistencia_equivalente):
    """
    Calcula el voltaje en un circuito paralelo.

    Args:
        corriente_total (float): La corriente total en amperios (A).
        resistencia_equivalente (float): La resistencia equivalente en ohmios (Ω).

    Returns:
        dict: Un diccionario con el voltaje en paralelo y el estado para animación.
    """
    voltaje_paralelo = corriente_total * resistencia_equivalente
    estado_animacion = {"corriente_total": corriente_total, "resistencia_equivalente": resistencia_equivalente, "voltaje_paralelo": voltaje_paralelo}
    return {"voltaje_paralelo": voltaje_paralelo, "estado_animacion": estado_animacion}

def calcular_corriente_paralelo(voltaje_total, resistencia_rama):
    """
    Calcula la corriente en una rama de un circuito paralelo.

    Args:
        voltaje_total (float): El voltaje total en voltios (V).
        resistencia_rama (float): La resistencia de la rama en ohmios (Ω).

    Returns:
        dict: Un diccionario con la corriente en la rama y el estado para animación.

    Raises:
        ValueError: Si la resistencia de la rama es cero.
    """
    if resistencia_rama == 0:
        raise ValueError("La resistencia de la rama no puede ser cero para calcular la corriente.")
    corriente_rama = voltaje_total / resistencia_rama
    estado_animacion = {"voltaje_total": voltaje_total, "resistencia_rama": resistencia_rama, "corriente_rama": corriente_rama}
    return {"corriente_rama": corriente_rama, "estado_animacion": estado_animacion}