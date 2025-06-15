from backend.Ecuaciones.energia.trabajo_energia import calcular_trabajo_energia_cinetica

def simular_trabajo_energia_cinetica(masa, fuerza, distancia, velocidad_inicial, angulo_fuerza_desplazamiento_grados):
    """
    Función API para simular el cálculo del trabajo y la energía cinética.
    """
    try:
        resultados = calcular_trabajo_energia_cinetica(masa, fuerza, distancia, velocidad_inicial, angulo_fuerza_desplazamiento_grados)
        return {
            "success": True,
            "message": "Cálculo de trabajo y energía cinética exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }