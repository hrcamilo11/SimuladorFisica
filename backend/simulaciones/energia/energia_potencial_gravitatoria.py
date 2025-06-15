from backend.Ecuaciones.energia.energia_potencial_gravitatoria import calcular_energia_potencial_gravitatoria

def simular_energia_potencial_gravitatoria(masa, altura_inicial, altura_final, velocidad_inicial):
    """
    Función API para simular el cálculo de la energía potencial gravitatoria.
    """
    try:
        resultados = calcular_energia_potencial_gravitatoria(masa, altura_inicial, altura_final, velocidad_inicial)
        return {
            "success": True,
            "message": "Cálculo de energía potencial gravitatoria exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }