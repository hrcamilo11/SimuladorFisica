from backend.Ecuaciones.energia.energia_potencial_elastica import calcular_energia_potencial_elastica

def simular_energia_potencial_elastica(masa, constante_elastica, amplitud, tiempo_total, num_puntos=100, fase_inicial_rad=0):
    """
    Función API para simular el cálculo de la energía potencial elástica.
    """
    try:
        resultados = calcular_energia_potencial_elastica(masa, constante_elastica, amplitud, tiempo_total, num_puntos, fase_inicial_rad)
        return {
            "success": True,
            "message": "Cálculo de energía potencial elástica exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }