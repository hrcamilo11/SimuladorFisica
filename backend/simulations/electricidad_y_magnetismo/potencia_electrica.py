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

def simular_potencia_electrica(voltaje, corriente):
    """
    Función API para simular el cálculo de la potencia eléctrica.
    """
    try:
        resultados = calcular_potencia_electrica(voltaje, corriente)
        return {
            "success": True,
            "message": "Cálculo de potencia eléctrica exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

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

def simular_energia_electrica(potencia, tiempo):
    """
    Función API para simular el cálculo de la energía eléctrica.
    """
    try:
        resultados = calcular_energia_electrica(potencia, tiempo)
        return {
            "success": True,
            "message": "Cálculo de energía eléctrica exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

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

def simular_voltaje_caida(corriente, resistencia):
    """
    Función API para simular el cálculo de la caída de voltaje.
    """
    try:
        resultados = calcular_voltaje_caida(corriente, resistencia)
        return {
            "success": True,
            "message": "Cálculo de caída de voltaje exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_eficiencia_electrica(potencia_salida, potencia_entrada):
    """
    Calcula la eficiencia eléctrica (η) dado la potencia de salida y la potencia de entrada.

    Args:
        potencia_salida (float): La potencia de salida en vatios (W).
        potencia_entrada (float): La potencia de entrada en vatios (W).

    Returns:
        dict: Un diccionario con la eficiencia eléctrica y el estado para animación.
    """
    if potencia_entrada == 0:
        raise ValueError("La potencia de entrada no puede ser cero.")
    eficiencia = potencia_salida / potencia_entrada
    estado_animacion = {"potencia_salida": potencia_salida, "potencia_entrada": potencia_entrada, "eficiencia": eficiencia}
    return {"eficiencia": eficiencia, "estado_animacion": estado_animacion}

def simular_eficiencia_electrica(potencia_salida, potencia_entrada):
    """
    Función API para simular el cálculo de la eficiencia eléctrica.
    """
    try:
        resultados = calcular_eficiencia_electrica(potencia_salida, potencia_entrada)
        return {
            "success": True,
            "message": "Cálculo de eficiencia eléctrica exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }