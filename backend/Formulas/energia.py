import numpy as np

def calcular_energia_cinetica(masa: float, velocidad: float) -> float:
    """
    Calcula la energía cinética (K) de un objeto.

    Args:
        masa (float): La masa del objeto (kg).
        velocidad (float): La velocidad del objeto (m/s).

    Returns:
        float: La energía cinética (Julios).

    Raises:
        ValueError: Si la masa es no positiva.
    """
    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")
    return 0.5 * masa * velocidad**2

def calcular_energia_potencial_elastica(constante_elastica, deformacion):
    """
    Calcula la energía potencial elástica.
    U_elastica = 0.5 * k * x^2
    """
    if constante_elastica <= 0:
        raise ValueError("La constante elástica debe ser positiva.")
    
    energia_potencial = 0.5 * constante_elastica * deformacion**2

    return {
        "energia_potencial": energia_potencial
    }

def calcular_energia_potencial_gravitatoria(masa, altura):
    """
    Calcula la energía potencial gravitatoria.
    U_g = m * g * h
    """
    g = 9.81  # Gravedad en m/s^2

    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")
    if altura < 0:
        raise ValueError("La altura no puede ser negativa.")

    energia_potencial = masa * g * altura

    return {
        "energia_potencial": energia_potencial
    }

def calcular_potencia(trabajo: float, tiempo: float) -> float:
    """
    Calcula la potencia (P) dado el trabajo realizado y el tiempo.

    Args:
        trabajo (float): El trabajo realizado (Julios).
        tiempo (float): El tiempo durante el cual se realiza el trabajo (s).

    Returns:
        float: La potencia (Watts).

    Raises:
        ValueError: Si el tiempo es no positivo.
    """
    if tiempo <= 0:
        raise ValueError("El tiempo debe ser un valor positivo.")
    return trabajo / tiempo

def calcular_potencia_velocidad(fuerza: float, velocidad: float) -> float:
    """
    Calcula la potencia (P) dado una fuerza y una velocidad constante.

    Args:
        fuerza (float): La fuerza aplicada (N).
        velocidad (float): La velocidad del objeto (m/s).

    Returns:
        float: La potencia (Watts).
    """
    return fuerza * velocidad

def calcular_trabajo_energia_cinetica(masa, velocidad_inicial, velocidad_final):
    """
    Calcula el trabajo realizado y el cambio en la energía cinética.
    W = ΔK
    ΔK = K_final - K_inicial
    K = 0.5 * m * v^2
    """
    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")

    # Energía cinética inicial
    energia_cinetica_inicial = 0.5 * masa * velocidad_inicial**2

    # Energía cinética final
    energia_cinetica_final = 0.5 * masa * velocidad_final**2

    # Trabajo realizado (cambio en la energía cinética)
    trabajo = energia_cinetica_final - energia_cinetica_inicial

    return {
        "trabajo": trabajo,
        "energia_cinetica_inicial": energia_cinetica_inicial,
        "energia_cinetica_final": energia_cinetica_final,
        "velocidad_inicial": velocidad_inicial,
        "velocidad_final": velocidad_final
    }