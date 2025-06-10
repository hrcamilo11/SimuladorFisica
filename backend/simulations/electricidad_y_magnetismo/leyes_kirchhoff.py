def calcular_ley_kirchhoff_voltaje(voltajes):
    """
    Calcula la suma de los voltajes en un lazo cerrado según la Ley de Voltajes de Kirchhoff.

    Args:
        voltajes (list): Una lista de voltajes en el lazo.

    Returns:
        dict: Un diccionario con la suma de los voltajes y el estado para animación.
    """
    suma_voltajes = sum(voltajes)
    estado_animacion = {"voltajes": voltajes, "suma_voltajes": suma_voltajes}
    return {"suma_voltajes": suma_voltajes, "estado_animacion": estado_animacion}

def simular_ley_kirchhoff_voltaje(voltajes):
    """
    Función API para simular el cálculo de la Ley de Voltajes de Kirchhoff.
    """
    try:
        resultados = calcular_ley_kirchhoff_voltaje(voltajes)
        return {
            "success": True,
            "message": "Cálculo de Ley de Voltajes de Kirchhoff exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_ley_kirchhoff_tension(corrientes):
    """
    Calcula la suma de las corrientes que entran y salen de un nodo según la Ley de Corrientes de Kirchhoff.

    Args:
        corrientes (list): Una lista de corrientes (entrantes positivas, salientes negativas).

    Returns:
        dict: Un diccionario con la suma de las corrientes y el estado para animación.
    """
    suma_corrientes = sum(corrientes)
    estado_animacion = {"corrientes": corrientes, "suma_corrientes": suma_corrientes}
    return {"suma_corrientes": suma_corrientes, "estado_animacion": estado_animacion}

def simular_ley_kirchhoff_tension(corrientes):
    """
    Función API para simular el cálculo de la Ley de Corrientes de Kirchhoff (tension).
    """
    try:
        resultados = calcular_ley_kirchhoff_tension(corrientes)
        return {
            "success": True,
            "message": "Cálculo de Ley de Corrientes de Kirchhoff (tensión) exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_ley_kirchhoff_corriente(corrientes_entrantes):
    """
    Calcula la corriente saliente total de un nodo utilizando la Ley de Corrientes de Kirchhoff (LCK).

    Args:
        corrientes_entrantes (list): Una lista de corrientes que entran al nodo en amperios (A).

    Returns:
        dict: Un diccionario con la corriente saliente y el estado para animación.
    """
    corriente_saliente = sum(corrientes_entrantes)
    estado_animacion = {"corrientes_entrantes": corrientes_entrantes, "corriente_saliente": corriente_saliente}
    return {"corriente_saliente": corriente_saliente, "estado_animacion": estado_animacion}

def simular_ley_kirchhoff_corriente(corrientes_entrantes):
    """
    Función API para simular el cálculo de la Ley de Corrientes de Kirchhoff (corriente).
    """
    try:
        resultados = calcular_ley_kirchhoff_corriente(corrientes_entrantes)
        return {
            "success": True,
            "message": "Cálculo de Ley de Corrientes de Kirchhoff (corriente) exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }