from backend.Ecuaciones.electricidad_y_magnetismo.capacitancia import calcular_capacitancia, calcular_carga_capacitor, calcular_voltaje_capacitor


def simular_capacitancia(carga, voltaje):
    """
    Función API para simular el cálculo de la capacitancia.
    """
    try:
        resultados = calcular_capacitancia(carga, voltaje)
        return {
            "success": True,
            "message": "Cálculo de capacitancia exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }


def simular_carga_capacitor(capacitancia, voltaje):
    """
    Función API para simular el cálculo de la carga en un capacitor.
    """
    try:
        resultados = calcular_carga_capacitor(capacitancia, voltaje)
        return {
            "success": True,
            "message": "Cálculo de carga en capacitor exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }


def simular_voltaje_capacitor(carga, capacitancia):
    """
    Función API para simular el cálculo del voltaje en un capacitor.
    """
    try:
        resultados = calcular_voltaje_capacitor(carga, capacitancia)
        return {
            "success": True,
            "message": "Cálculo de voltaje en capacitor exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }


from backend.Ecuaciones.electricidad_y_magnetismo.capacitancia import calcular_energia_capacitor

def simular_energia_capacitor(capacitancia, voltaje):
    """
    Función API para simular el cálculo de la energía en un capacitor.
    """
    try:
        resultados = calcular_energia_capacitor(capacitancia, voltaje)
        return {
            "success": True,
            "message": "Cálculo de energía en capacitor exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }