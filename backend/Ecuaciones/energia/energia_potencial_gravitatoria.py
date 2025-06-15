import numpy as np

def calcular_energia_potencial_gravitatoria(masa, altura_inicial, altura_final, velocidad_inicial):
    """
    Calcula la energía potencial gravitatoria y la conservación de la energía mecánica.
    U_g = m * g * h
    K = 0.5 * m * v^2
    E_m = U_g + K
    """
    g = 9.81  # Gravedad en m/s^2

    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")

    # Energías iniciales
    energia_potencial_inicial = masa * g * altura_inicial
    energia_cinetica_inicial = 0.5 * masa * velocidad_inicial**2
    energia_mecanica_inicial = energia_potencial_inicial + energia_cinetica_inicial

    # Energías finales (asumiendo conservación de la energía mecánica)
    energia_mecanica_final = energia_mecanica_inicial
    energia_potencial_final = masa * g * altura_final
    energia_cinetica_final = energia_mecanica_final - energia_potencial_final

    # Velocidad final
    if energia_cinetica_final < 0: # Esto puede ocurrir si la altura final es demasiado alta
        velocidad_final = 0.0 # El objeto no alcanza esa altura o se detiene
    else:
        velocidad_final = np.sqrt(2 * energia_cinetica_final / masa)

    estado_animacion = {
        "altura_inicial": altura_inicial,
        "altura_final": altura_final,
        "velocidad_inicial": velocidad_inicial,
        "velocidad_final": velocidad_final,
        "energia_potencial_inicial": energia_potencial_inicial,
        "energia_cinetica_inicial": energia_cinetica_inicial,
        "energia_mecanica_inicial": energia_mecanica_inicial,
        "energia_potencial_final": energia_potencial_final,
        "energia_cinetica_final": energia_cinetica_final,
        "energia_mecanica_final": energia_mecanica_final
    }

    return {
        "energia_potencial_inicial": energia_potencial_inicial,
        "energia_cinetica_inicial": energia_cinetica_inicial,
        "energia_mecanica_inicial": energia_mecanica_inicial,
        "energia_potencial_final": energia_potencial_final,
        "energia_cinetica_final": energia_cinetica_final,
        "energia_mecanica_final": energia_mecanica_final,
        "velocidad_final": velocidad_final,
        "estado_animacion": estado_animacion
    }