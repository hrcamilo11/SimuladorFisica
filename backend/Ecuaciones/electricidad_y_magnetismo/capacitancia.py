def calcular_capacitancia(carga, voltaje):
    """
    Calcula la capacitancia (C) dado la carga (Q) y el voltaje (V).

    Args:
        carga (float): La carga en culombios (C).
        voltaje (float): El voltaje en voltios (V).

    Returns:
        dict: Un diccionario con la capacitancia y el estado para animación.

    Raises:
        ValueError: Si el voltaje es cero.
    """
    if voltaje == 0:
        raise ValueError("El voltaje no puede ser cero.")
    capacitancia = carga / voltaje
    estado_animacion = {"carga": carga, "voltaje": voltaje, "capacitancia": capacitancia}
    return {"capacitancia": capacitancia, "estado_animacion": estado_animacion}

def calcular_carga_capacitor(capacitancia, voltaje):
    """
    Calcula la carga (Q) en un capacitor dado su capacitancia (C) y el voltaje (V).

    Args:
        capacitancia (float): La capacitancia en faradios (F).
        voltaje (float): El voltaje en voltios (V).

    Returns:
        dict: Un diccionario con la carga y el estado para animación.
    """
    carga = capacitancia * voltaje
    estado_animacion = {"capacitancia": capacitancia, "voltaje": voltaje, "carga": carga}
    return {"carga": carga, "estado_animacion": estado_animacion}

def calcular_voltaje_capacitor(carga, capacitancia):
    """
    Calcula el voltaje (V) en un capacitor dado la carga (Q) y la capacitancia (C).

    Args:
        carga (float): La carga en culombios (C).
        capacitancia (float): La capacitancia en faradios (F).

    Returns:
        dict: Un diccionario con el voltaje y el estado para animación.

    Raises:
        ValueError: Si la capacitancia es cero.
    """
    if capacitancia == 0:
        raise ValueError("La capacitancia no puede ser cero.")
    voltaje = carga / capacitancia
    estado_animacion = {"carga": carga, "capacitancia": capacitancia, "voltaje": voltaje}
    return {"voltaje": voltaje, "estado_animacion": estado_animacion}

def calcular_energia_capacitor(capacitancia, voltaje):
    """
    Calcula la energía almacenada (U) en un capacitor.

    Args:
        capacitancia (float): La capacitancia en faradios (F).
        voltaje (float): El voltaje en voltios (V).

    Returns:
        dict: Un diccionario con la energía y el estado para animación.
    """
    energia = 0.5 * capacitancia * (voltaje ** 2)
    estado_animacion = {"capacitancia": capacitancia, "voltaje": voltaje, "energia": energia}
    return {"energia": energia, "estado_animacion": estado_animacion}