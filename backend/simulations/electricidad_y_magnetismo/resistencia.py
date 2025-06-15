from backend.Ecuaciones.electricidad_y_magnetismo.resistencia import calcular_resistencia


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