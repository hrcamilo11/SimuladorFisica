import numpy as np

from backend.Ecuaciones.dinamica.leyes_newton import calcular_fuerzas_leyes_newton

def simular_leyes_newton(masa, fuerza_aplicada, angulo_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico, tiempo_total, num_puntos=100):
    """
    Función API para simular las Leyes de Newton.
    """
    try:
        resultados = calcular_fuerzas_leyes_newton(masa, fuerza_aplicada, angulo_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico, tiempo_total, num_puntos)
        return {
            "success": True,
            "message": "Simulación de Leyes de Newton exitosa.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }