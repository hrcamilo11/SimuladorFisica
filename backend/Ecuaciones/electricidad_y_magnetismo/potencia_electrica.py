def calcular_potencia_electrica(voltaje, corriente):
    """
    Calcula la potencia eléctrica (P) dado el voltaje (V) y la corriente (I).

    Args:
        voltaje (float): El voltaje en voltios (V).
        corriente (float): La corriente en amperios (A).

    Returns:
        dict: Un diccionario con la potencia eléctrica y el estado para animación.
    """
    potencia = voltaje * corriente
    estado_animacion = {"voltaje": voltaje, "corriente": corriente, "potencia": potencia}
    return {"potencia": potencia, "estado_animacion": estado_animacion}

def calcular_energia_electrica(potencia, tiempo):
    """
    Calcula la energía eléctrica consumida.

    Args:
        potencia (float): La potencia en vatios (W).
        tiempo (float): El tiempo en horas (h).

    Returns:
        dict: Un diccionario con la energía eléctrica y el estado para animación.
    """
    energia = (potencia * tiempo) / 1000
    estado_animacion = {"potencia": potencia, "tiempo": tiempo, "energia": energia}
    return {"energia": energia, "estado_animacion": estado_animacion}

def calcular_voltaje_caida(corriente, resistencia):
    """
    Calcula la caída de voltaje en un circuito.

    Args:
        corriente (float): La corriente en amperios (A).
        resistencia (float): La resistencia en ohmios (Ω).

    Returns:
        dict: Un diccionario con la caída de voltaje y el estado para animación.
    """
    voltaje_caida = corriente * resistencia
    estado_animacion = {"corriente": corriente, "resistencia": resistencia, "voltaje_caida": voltaje_caida}
    return {"voltaje_caida": voltaje_caida, "estado_animacion": estado_animacion}

def calcular_eficiencia_electrica(potencia_salida, potencia_entrada):
    """
    Calcula la eficiencia eléctrica de un sistema.

    Args:
        potencia_salida (float): La potencia de salida en vatios (W).
        potencia_entrada (float): La potencia de entrada en vatios (W).

    Returns:
        dict: Un diccionario con la eficiencia eléctrica y el estado para animación.

    Raises:
        ValueError: Si la potencia de entrada es cero.
    """
    if potencia_entrada == 0:
        raise ValueError("La potencia de entrada no puede ser cero.")
    eficiencia = (potencia_salida / potencia_entrada) * 100
    estado_animacion = {"potencia_salida": potencia_salida, "potencia_entrada": potencia_entrada, "eficiencia": eficiencia}
    return {"eficiencia": eficiencia, "estado_animacion": estado_animacion}