import math
import numpy as np

GRAVEDAD = 9.81  # m/s^2

def calcular_fuerza_neta(masa: float, aceleracion: float) -> float:
    """
    Calcula la fuerza neta aplicada a un objeto.
    F = m * a
    """
    return masa * aceleracion

def calcular_aceleracion(fuerza_neta: float, masa: float) -> float:
    """
    Calcula la aceleración de un objeto dada la fuerza neta y la masa.
    a = F / m
    """
    if masa == 0:
        raise ValueError("La masa no puede ser cero.")
    return fuerza_neta / masa

def calcular_fuerza_rozamiento_estatico(coeficiente_rozamiento_estatico: float, fuerza_normal: float) -> float:
    """
    Calcula la fuerza de rozamiento estático máxima.
    Fs_max = mu_s * N
    """
    return coeficiente_rozamiento_estatico * fuerza_normal

def calcular_fuerza_rozamiento_cinetico(coeficiente_rozamiento_cinetico: float, fuerza_normal: float) -> float:
    """
    Calcula la fuerza de rozamiento cinético.
    Fk = mu_k * N
    """
    return coeficiente_rozamiento_cinetico * fuerza_normal

def calcular_tension_plano_inclinado_polea(masa1: float, masa2: float, angulo_inclinacion_grados: float, coeficiente_rozamiento_cinetico: float) -> float:
    """
    Calcula la tensión en un sistema de plano inclinado con polea.
    """
    g = GRAVEDAD  # Aceleración debido a la gravedad en m/s^2
    angulo_rad = math.radians(angulo_inclinacion_grados)

    if (masa1 + masa2) == 0:
        raise ValueError("La suma de las masas no puede ser cero.")

    aceleracion = (masa2 * g - masa1 * g * math.sin(angulo_rad) - coeficiente_rozamiento_cinetico * masa1 * g * math.cos(angulo_rad)) / (masa1 + masa2)
    tension = masa2 * g - masa2 * aceleracion
    return tension

def calcular_aceleracion_plano_inclinado_polea(masa1: float, masa2: float, angulo_inclinacion_grados: float, coeficiente_rozamiento_cinetico: float) -> float:
    """
    Calcula la aceleración en un sistema de plano inclinado con polea.
    """
    g = GRAVEDAD  # Aceleración debido a la gravedad en m/s^2
    angulo_rad = math.radians(angulo_inclinacion_grados)

    if (masa1 + masa2) == 0:
        raise ValueError("La suma de las masas no puede ser cero.")

    aceleracion = (masa2 * g - masa1 * g * math.sin(angulo_rad) - coeficiente_rozamiento_cinetico * masa1 * g * math.cos(angulo_rad)) / (masa1 + masa2)
    return aceleracion

def calcular_fuerzas_leyes_newton(masa, fuerza_aplicada, angulo_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico):
    """
    Calcula las fuerzas y el movimiento de un objeto en un plano horizontal,
    considerando las Leyes de Newton y la fuerza de rozamiento.
    """
    g = GRAVEDAD  # Gravedad en m/s^2
    angulo_rad = np.deg2rad(angulo_grados)

    # Componentes de la fuerza aplicada
    fuerza_x = fuerza_aplicada * np.cos(angulo_rad)
    fuerza_y = fuerza_aplicada * np.sin(angulo_rad)

    # Fuerza normal
    fuerza_normal = masa * g - fuerza_y
    if fuerza_normal < 0: # Objeto levantado
        fuerza_normal = 0

    # Fuerza de rozamiento estático máxima
    fuerza_rozamiento_estatico_max = coeficiente_rozamiento_estatico * fuerza_normal

    # Determinar si hay movimiento y calcular la aceleración
    if abs(fuerza_x) <= fuerza_rozamiento_estatico_max:
        aceleracion = 0.0
        fuerza_neta = 0.0
        fuerza_rozamiento = fuerza_x # La fuerza de rozamiento iguala a la fuerza aplicada para mantener el equilibrio
    else:
        # Hay movimiento, calcular fuerza de rozamiento cinético
        fuerza_rozamiento_cinetico_val = coeficiente_rozamiento_cinetico * fuerza_normal
        fuerza_rozamiento = np.sign(fuerza_x) * fuerza_rozamiento_cinetico_val
        fuerza_neta = fuerza_x - fuerza_rozamiento
        aceleracion = fuerza_neta / masa

    return {
        "fuerza_normal": fuerza_normal,
        "fuerza_rozamiento_estatico_max": fuerza_rozamiento_estatico_max,
        "fuerza_rozamiento": fuerza_rozamiento,
        "fuerza_neta": fuerza_neta,
        "aceleracion": aceleracion
    }

def calcular_plano_inclinado(masa, angulo_inclinacion_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico):
    """
    Calcula las fuerzas y aceleración de un objeto sobre un plano inclinado.
    """
    angulo_inclinacion_rad = np.deg2rad(angulo_inclinacion_grados)

    # Componentes de la gravedad
    g_paralela = GRAVEDAD * np.sin(angulo_inclinacion_rad)
    g_perpendicular = GRAVEDAD * np.cos(angulo_inclinacion_rad)

    # Fuerza normal
    fuerza_normal = masa * g_perpendicular

    # Fuerza de rozamiento estático máxima
    fuerza_rozamiento_estatico_max = calcular_fuerza_rozamiento_estatico(coeficiente_rozamiento_estatico, fuerza_normal)

    # Fuerza neta sin rozamiento
    fuerza_neta_sin_rozamiento = masa * g_paralela

    aceleracion = 0.0
    fuerza_rozamiento = 0.0
    fuerza_neta = 0.0
    mensaje = ""

    if fuerza_neta_sin_rozamiento <= fuerza_rozamiento_estatico_max:
        # El objeto permanece en reposo
        aceleracion = 0.0
        fuerza_neta = 0.0
        fuerza_rozamiento = fuerza_neta_sin_rozamiento # La fuerza de rozamiento iguala a la fuerza aplicada para mantener el equilibrio
        mensaje = "El objeto permanece en reposo."
    else:
        # Se mueve, aplicar rozamiento cinético
        fuerza_rozamiento = calcular_fuerza_rozamiento_cinetico(coeficiente_rozamiento_cinetico, fuerza_normal)
        fuerza_neta = fuerza_neta_sin_rozamiento - fuerza_rozamiento
        aceleracion = fuerza_neta / masa
        mensaje = "El objeto se desliza por el plano."

    return {
        "fuerza_normal": fuerza_normal,
        "fuerza_rozamiento_estatico_max": fuerza_rozamiento_estatico_max,
        "fuerza_rozamiento": fuerza_rozamiento,
        "fuerza_neta": fuerza_neta,
        "aceleracion": aceleracion,
        "mensaje": mensaje
    }


def calcular_plano_inclinado_polea_formulas(
    masa1: float,
    masa2: float,
    angulo_inclinacion_grados: float,
    coeficiente_rozamiento_cinetico: float,
    gravedad: float = 9.81
):
    """
    Calcula la aceleración y la tensión en un sistema de plano inclinado con polea.

    Args:
        masa1 (float): Masa del objeto en el plano inclinado (kg).
        masa2 (float): Masa del objeto colgante (kg).
        angulo_inclinacion_grados (float): Ángulo del plano inclinado en grados.
        coeficiente_rozamiento_cinetico (float): Coeficiente de rozamiento cinético entre masa1 y el plano.
        gravedad (float): Aceleración debido a la gravedad (m/s^2).

    Returns:
        dict: Un diccionario con la aceleración y la tensión del sistema.
    """

    angulo_rad = np.radians(angulo_inclinacion_grados)

    # Determinamos la dirección inicial del movimiento o la tendencia
    # Fuerza que tira masa1 hacia abajo del plano: m1*g*sin(angulo_rad)
    # Fuerza de rozamiento máxima estática (si fuera el caso): mu_s * m1*g*cos(angulo_rad)
    # Fuerza que tira masa2 hacia abajo: m2*g

    # Consideramos el movimiento si masa2 tira de masa1 hacia arriba del plano
    fuerza_neta_potencial_arriba = masa2 * gravedad - (masa1 * gravedad * np.sin(angulo_rad) + coeficiente_rozamiento_cinetico * masa1 * gravedad * np.cos(angulo_rad))

    # Consideramos el movimiento si masa1 se desliza hacia abajo del plano (y tira de masa2 hacia arriba)
    fuerza_neta_potencial_abajo = (masa1 * gravedad * np.sin(angulo_rad) - coeficiente_rozamiento_cinetico * masa1 * gravedad * np.cos(angulo_rad)) - masa2 * gravedad

    aceleracion = 0.0
    tension = 0.0

    if fuerza_neta_potencial_arriba > 0:
        # Masa2 tira de masa1 hacia arriba del plano
        aceleracion = fuerza_neta_potencial_arriba / (masa1 + masa2)
        tension = masa2 * gravedad - masa2 * aceleracion
    elif fuerza_neta_potencial_abajo > 0:
        # Masa1 se desliza hacia abajo del plano
        aceleracion = fuerza_neta_potencial_abajo / (masa1 + masa2)
        tension = masa2 * gravedad + masa2 * aceleracion # Tensión es mayor si masa2 acelera hacia arriba
    else:
        # El sistema está en equilibrio o la fuerza neta es cero
        aceleracion = 0.0
        tension = masa2 * gravedad # Si no hay movimiento, la tensión equilibra el peso de masa2
        if masa1 * gravedad * np.sin(angulo_rad) > masa2 * gravedad:
            tension = masa1 * gravedad * np.sin(angulo_rad) - coeficiente_rozamiento_cinetico * masa1 * gravedad * np.cos(angulo_rad)
        else:
            tension = masa2 * gravedad

    return {
        'aceleracion': aceleracion,
        'tension': tension
    }