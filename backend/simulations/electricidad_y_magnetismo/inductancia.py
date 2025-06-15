from backend.Ecuaciones.electricidad_y_magnetismo.inductancia import calcular_inductancia, calcular_energia_inductor


def simular_inductancia(flujo_magnetico, corriente, numero_espiras):
    """
    Función API para simular el cálculo de la inductancia.
    """
    try:
        resultados = calcular_inductancia(flujo_magnetico, corriente, numero_espiras)
        return {
            "success": True,
            "message": "Cálculo de inductancia exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }


def simular_energia_inductor(inductancia, corriente):
    """
    Función API para simular el cálculo de la energía en un inductor.
    """
    try:
        resultados = calcular_energia_inductor(inductancia, corriente)
        return {
            "success": True,
            "message": "Cálculo de energía en inductor exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }