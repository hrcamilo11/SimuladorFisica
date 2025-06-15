from backend.Ecuaciones.electricidad_y_magnetismo.potencia_electrica import calcular_potencia_electrica, calcular_energia_electrica, calcular_voltaje_caida, calcular_eficiencia_electrica


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