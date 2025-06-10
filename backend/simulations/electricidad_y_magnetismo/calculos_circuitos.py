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

def simular_circuito_serie(resistencias):
    """
    Función API para simular el cálculo de resistencia en un circuito en serie.
    """
    try:
        resultados = calcular_circuito_serie(resistencias)
        return {
            "success": True,
            "message": "Cálculo de resistencia en serie exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }



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

def simular_circuito_paralelo(resistencias):
    """
    Función API para simular el cálculo de resistencia en un circuito en paralelo.
    """
    try:
        resultados = calcular_circuito_paralelo(resistencias)
        return {
            "success": True,
            "message": "Cálculo de resistencia en paralelo exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

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

def simular_corriente_total(voltaje_total, resistencia_total):
    """
    Función API para simular el cálculo de la corriente total.
    """
    try:
        resultados = calcular_corriente_total(voltaje_total, resistencia_total)
        return {
            "success": True,
            "message": "Cálculo de corriente total exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_voltaje_en_resistencia(corriente, resistencia):
    """
    Calcula el voltaje a través de una resistencia usando la Ley de Ohm.

    Args:
        corriente (float): La corriente que pasa por la resistencia en amperios (A).
        resistencia (float): El valor de la resistencia en ohmios (Ω).

    Returns:
        dict: Un diccionario con el voltaje y el estado para animación.
    """
    voltaje = corriente * resistencia
    estado_animacion = {"corriente": corriente, "resistencia": resistencia, "voltaje": voltaje}
    return {"voltaje": voltaje, "estado_animacion": estado_animacion}

def simular_voltaje_en_resistencia(corriente, resistencia):
    """
    Función API para simular el cálculo del voltaje en una resistencia.
    """
    try:
        resultados = calcular_voltaje_en_resistencia(corriente, resistencia)
        return {
            "success": True,
            "message": "Cálculo de voltaje en resistencia exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_potencia_en_resistencia(corriente, voltaje):
    """
    Calcula la potencia disipada por una resistencia.

    Args:
        corriente (float): La corriente que pasa por la resistencia en amperios (A).
        voltaje (float): El voltaje a través de la resistencia en voltios (V).

    Returns:
        dict: Un diccionario con la potencia y el estado para animación.
    """
    potencia = corriente * voltaje
    estado_animacion = {"corriente": corriente, "voltaje": voltaje, "potencia": potencia}
    return {"potencia": potencia, "estado_animacion": estado_animacion}

def simular_potencia_en_resistencia(corriente, voltaje):
    """
    Función API para simular el cálculo de la potencia en una resistencia.
    """
    try:
        resultados = calcular_potencia_en_resistencia(corriente, voltaje)
        return {
            "success": True,
            "message": "Cálculo de potencia en resistencia exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_resistencia_equivalente_serie(resistencias):
    """
    Calcula la resistencia equivalente de resistencias en serie.

    Args:
        resistencias (list): Una lista de valores de resistencia en ohmios (Ω).

    Returns:
        dict: Un diccionario con la resistencia equivalente y el estado para animación.
    """
    resistencia_equivalente = sum(resistencias)
    estado_animacion = {"resistencias": resistencias, "resistencia_equivalente": resistencia_equivalente}
    return {"resistencia_equivalente": resistencia_equivalente, "estado_animacion": estado_animacion}

def simular_resistencia_equivalente_serie(resistencias):
    """
    Función API para simular el cálculo de resistencia equivalente en serie.
    """
    try:
        resultados = calcular_resistencia_equivalente_serie(resistencias)
        return {
            "success": True,
            "message": "Cálculo de resistencia equivalente en serie exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }