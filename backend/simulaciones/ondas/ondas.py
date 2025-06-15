from backend.Ecuaciones.ondas.ondas import calcular_longitud_onda, calcular_frecuencia_onda, calcular_velocidad_onda

def simular_longitud_onda(velocidad, frecuencia):
    """
    Función API para simular el cálculo de la longitud de onda.
    """
    try:
        resultados = calcular_longitud_onda(velocidad, frecuencia)
        return {
            "success": True,
            "message": "Cálculo de longitud de onda exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def simular_frecuencia_onda(velocidad, longitud_onda):
    """
    Función API para simular el cálculo de la frecuencia de onda.
    """
    try:
        resultados = calcular_frecuencia_onda(velocidad, longitud_onda)
        return {
            "success": True,
            "message": "Cálculo de frecuencia de onda exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def simular_velocidad_onda(longitud_onda, frecuencia):
    """
    Función API para simular el cálculo de la velocidad de onda.
    """
    try:
        resultados = calcular_velocidad_onda(longitud_onda, frecuencia)
        return {
            "success": True,
            "message": "Cálculo de velocidad de onda exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }