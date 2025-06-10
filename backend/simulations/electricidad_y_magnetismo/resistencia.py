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

def simular_resistencia(voltaje, corriente):
    """
    Función API para simular el cálculo de la resistencia.
    """
    try:
        resultados = calcular_resistencia(voltaje, corriente)
        return {
            "success": True,
            "message": "Cálculo de resistencia exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }