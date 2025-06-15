import numpy as np

from backend.Ecuaciones.dinamica.plano_inclinado import calcular_plano_inclinado

GRAVEDAD = 9.81  # m/s^2

def simular_plano_inclinado(masa, angulo_inclinacion_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico, distancia_plano, velocidad_inicial=0, num_puntos=100):
    """
    Función API para simular el movimiento en un plano inclinado.
    """
    try:
        resultados = calcular_plano_inclinado(masa, angulo_inclinacion_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico, distancia_plano, velocidad_inicial, num_puntos)
        return {
            "success": True,
            "message": "Simulación de Plano Inclinado exitosa.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }