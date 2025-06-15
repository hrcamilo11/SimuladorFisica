from backend.Ecuaciones.electricidad_y_magnetismo.ley_ohm import calcular_ley_ohm, calcular_potencia_ohm


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