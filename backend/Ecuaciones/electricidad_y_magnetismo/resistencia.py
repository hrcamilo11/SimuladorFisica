def calcular_resistencia(voltaje, corriente):
    """
    Calcula la resistencia utilizando la Ley de Ohm.

    Args:
        voltaje (float): El voltaje en voltios (V).
        corriente (float): La corriente en amperios (A).

    Returns:
        dict: Un diccionario con la resistencia y el estado para animación.
    """
    if corriente == 0:
        raise ValueError("La corriente no puede ser cero para calcular la resistencia.")
    resistencia = voltaje / corriente
    estado_animacion = {"voltaje": voltaje, "corriente": corriente, "resistencia": resistencia}
    return {"resistencia": resistencia, "estado_animacion": estado_animacion}