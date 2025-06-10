import numpy as np

def calcular_trabajo_energia_cinetica(masa, fuerza, distancia, velocidad_inicial, angulo_fuerza_desplazamiento_grados):
    """
    Calcula el trabajo realizado por una fuerza y el cambio en la energía cinética.
    W = F * d * cos(theta)
    ΔK = W
    K = 0.5 * m * v^2
    """
    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")
    if distancia < 0:
        raise ValueError("La distancia no puede ser negativa.")

    angulo_rad = np.deg2rad(angulo_fuerza_desplazamiento_grados)

    # Trabajo realizado por la fuerza
    trabajo = fuerza * distancia * np.cos(angulo_rad)

    # Energía cinética inicial
    energia_cinetica_inicial = 0.5 * masa * velocidad_inicial**2

    # Energía cinética final (usando el teorema del trabajo y la energía)
    energia_cinetica_final = energia_cinetica_inicial + trabajo

    # Velocidad final
    if energia_cinetica_final < 0: # Esto podría pasar si el trabajo es muy negativo y la K inicial pequeña
        velocidad_final = 0.0 # El objeto se detiene
    else:
        velocidad_final = np.sqrt(2 * energia_cinetica_final / masa)

    estado_animacion = {
        "fuerza": fuerza,
        "distancia": distancia,
        "velocidad_inicial": velocidad_inicial,
        "angulo_fuerza_desplazamiento_grados": angulo_fuerza_desplazamiento_grados,
        "trabajo": trabajo,
        "energia_cinetica_inicial": energia_cinetica_inicial,
        "energia_cinetica_final": energia_cinetica_final,
        "velocidad_final": velocidad_final
    }

    return {
        "trabajo": trabajo,
        "energia_cinetica_inicial": energia_cinetica_inicial,
        "energia_cinetica_final": energia_cinetica_final,
        "velocidad_final": velocidad_final,
        "estado_animacion": estado_animacion
    }

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