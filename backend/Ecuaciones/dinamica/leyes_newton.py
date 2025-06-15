import numpy as np

def calcular_fuerzas_leyes_newton(masa, fuerza_aplicada, angulo_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico, tiempo_total, num_puntos=100):
    """
    Calcula las fuerzas y el movimiento de un objeto en un plano horizontal,
    considerando las Leyes de Newton y la fuerza de rozamiento.
    """
    g = 9.81  # Gravedad en m/s^2
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
        fuerza_rozamiento = -fuerza_x # La fuerza de rozamiento se opone a la fuerza aplicada para mantener el equilibrio
    else:
        # Hay movimiento, calcular fuerza de rozamiento cinético
        fuerza_rozamiento_cinetico = coeficiente_rozamiento_cinetico * fuerza_normal
        fuerza_rozamiento = np.sign(fuerza_x) * fuerza_rozamiento_cinetico
        fuerza_neta = fuerza_x - fuerza_rozamiento
        aceleracion = fuerza_neta / masa

    # Calcular posición y velocidad a lo largo del tiempo
    if tiempo_total < 0:
        raise ValueError("El tiempo total no puede ser negativo.")
    if num_puntos <= 1 and tiempo_total > 0:
        num_puntos = 2
    elif num_puntos < 1:
        num_puntos = 1

    tiempos = np.linspace(0, tiempo_total, num_puntos)
    posiciones = 0.5 * aceleracion * tiempos**2  # Asumiendo posición inicial 0
    velocidades = aceleracion * tiempos          # Asumiendo velocidad inicial 0

    estado_animacion = []
    for i in range(num_puntos):
        estado_animacion.append([tiempos[i], posiciones[i], velocidades[i]])

    return {
        "fuerza_normal": fuerza_normal,
        "fuerza_rozamiento_estatico_max": fuerza_rozamiento_estatico_max,
        "fuerza_rozamiento": fuerza_rozamiento,
        "fuerza_neta": fuerza_neta,
        "aceleracion": aceleracion,
        "tiempos": list(tiempos),
        "posiciones": list(posiciones),
        "velocidades": list(velocidades),
        "estado_animacion": estado_animacion
    }