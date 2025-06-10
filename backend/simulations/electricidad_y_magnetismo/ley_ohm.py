def calcular_ley_ohm(voltaje=None, corriente=None, resistencia=None):
    """
    Calcula el voltaje, la corriente o la resistencia utilizando la Ley de Ohm (V = I * R).

    Args:
        voltaje (float, optional): El voltaje en voltios (V). Defaults to None.
        corriente (float, optional): La corriente en amperios (A). Defaults to None.
        resistencia (float, optional): La resistencia en ohmios (Ω). Defaults to None.

    Returns:
        dict: Un diccionario con el valor calculado y el estado para animación.

    Raises:
        ValueError: Si se proporcionan menos de dos argumentos o si la resistencia es cero al calcular la corriente.
    """
    if sum([voltaje is not None, corriente is not None, resistencia is not None]) != 2:
        raise ValueError("Debe proporcionar exactamente dos de los tres valores (voltaje, corriente, resistencia).")

    if voltaje is None:
        valor_calculado = corriente * resistencia
        estado_animacion = {"corriente": corriente, "resistencia": resistencia, "voltaje": valor_calculado}
    elif corriente is None:
        if resistencia == 0:
            raise ValueError("La resistencia no puede ser cero al calcular la corriente.")
        valor_calculado = voltaje / resistencia
        estado_animacion = {"voltaje": voltaje, "resistencia": resistencia, "corriente": valor_calculado}
    else:
        if corriente == 0:
            raise ValueError("La corriente no puede ser cero al calcular la resistencia.")
        valor_calculado = voltaje / corriente
        estado_animacion = {"voltaje": voltaje, "corriente": corriente, "resistencia": valor_calculado}

    return {"valor_calculado": valor_calculado, "estado_animacion": estado_animacion}

def simular_ley_ohm(voltaje=None, corriente=None, resistencia=None):
    """
    Función API para simular el cálculo de la Ley de Ohm.
    """
    try:
        resultados = calcular_ley_ohm(voltaje, corriente, resistencia)
        return {
            "success": True,
            "message": "Cálculo de Ley de Ohm exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_potencia_ohm(voltaje=None, corriente=None, resistencia=None):
    """
    Calcula la potencia (P) utilizando la Ley de Ohm (P = V*I, P = I^2*R, P = V^2/R).

    Args:
        voltaje (float, optional): El voltaje en voltios (V).
        corriente (float, optional): La corriente en amperios (A).
        resistencia (float, optional): La resistencia en ohmios (Ω).

    Returns:
        dict: Un diccionario con la potencia y el estado para animación.

    Raises:
        ValueError: Si no se proporcionan suficientes parámetros para el cálculo.
    """
    if voltaje is not None and corriente is not None:
        potencia = voltaje * corriente
        estado_animacion = {"voltaje": voltaje, "corriente": corriente, "potencia": potencia}
    elif corriente is not None and resistencia is not None:
        potencia = (corriente ** 2) * resistencia
        estado_animacion = {"corriente": corriente, "resistencia": resistencia, "potencia": potencia}
    elif voltaje is not None and resistencia is not None:
        if resistencia == 0:
            raise ValueError("La resistencia no puede ser cero cuando se calcula la potencia con voltaje y resistencia.")
        potencia = (voltaje ** 2) / resistencia
        estado_animacion = {"voltaje": voltaje, "resistencia": resistencia, "potencia": potencia}
    else:
        raise ValueError("Se requieren al menos dos de los tres parámetros (voltaje, corriente, resistencia) para calcular la potencia.")
    
    return {"potencia": potencia, "estado_animacion": estado_animacion}

def simular_potencia_ohm(voltaje=None, corriente=None, resistencia=None):
    """
    Función API para simular el cálculo de la potencia utilizando la Ley de Ohm.
    """
    try:
        resultados = calcular_potencia_ohm(voltaje, corriente, resistencia)
        return {
            "success": True,
            "message": "Cálculo de potencia exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }