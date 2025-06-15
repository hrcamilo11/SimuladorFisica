import numpy as np

GRAVEDAD = 9.81  # m/s^2

def calcular_plano_inclinado(masa, angulo_inclinacion_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico, distancia_plano, velocidad_inicial=0, num_puntos=100):
    """
    Calcula el movimiento de un objeto sobre un plano inclinado.
    Retorna tiempos, posiciones, velocidades y aceleraciones.
    """
    angulo_inclinacion_rad = np.deg2rad(angulo_inclinacion_grados)

    # Componentes de la gravedad
    g_paralela = GRAVEDAD * np.sin(angulo_inclinacion_rad)
    g_perpendicular = GRAVEDAD * np.cos(angulo_inclinacion_rad)

    # Fuerza normal
    fuerza_normal = masa * g_perpendicular

    # Fuerza de rozamiento estático máxima
    fuerza_rozamiento_estatico_max = coeficiente_rozamiento_estatico * fuerza_normal

    # Fuerza neta sin rozamiento
    fuerza_neta_sin_rozamiento = masa * g_paralela

    # Determinar si el objeto se mueve
    if fuerza_neta_sin_rozamiento <= fuerza_rozamiento_estatico_max and velocidad_inicial == 0:
        # El objeto permanece en reposo
        return [0, 1], [0, 0], [0, 0], [0, 0], "El objeto permanece en reposo."

    # Si se mueve o la fuerza neta supera el rozamiento estático
    aceleracion = g_paralela
    mensaje = ""

    if fuerza_neta_sin_rozamiento > fuerza_rozamiento_estatico_max or velocidad_inicial > 0:
        # Se mueve, aplicar rozamiento cinético
        fuerza_rozamiento_cinetico = coeficiente_rozamiento_cinetico * fuerza_normal
        aceleracion = g_paralela - (fuerza_rozamiento_cinetico / masa)
        mensaje = "El objeto se desliza por el plano."
        if aceleracion < 0: # Si la aceleración es negativa, significa que el rozamiento lo detiene
            aceleracion = 0 # O se detiene, o se mueve en la otra dirección (no contemplado aquí)
            mensaje = "El objeto se detiene debido al rozamiento."
    else:
        mensaje = "El objeto permanece en reposo."
        return [0, 1], [0, 0], [0, 0], [0, 0], mensaje

    # Simulación del movimiento
    tiempos = np.linspace(0, 5, num_puntos) # Tiempo inicial, se ajustará dinámicamente
    posiciones = []
    velocidades = []
    tiempos_reales = []

    t_actual = 0
    v_actual = velocidad_inicial
    x_actual = 0
    dt = tiempos[1] - tiempos[0] if len(tiempos) > 1 else 0.05 # Paso de tiempo

    for i in range(num_puntos):
        if x_actual >= distancia_plano:
            break

        posiciones.append(x_actual)
        velocidades.append(v_actual)
        tiempos_reales.append(t_actual)

        # Actualizar estado
        x_actual += v_actual * dt + 0.5 * aceleracion * dt**2
        v_actual += aceleracion * dt
        t_actual += dt

        if v_actual < 0: # Si la velocidad se vuelve negativa, se detiene
            v_actual = 0
            aceleracion = 0
            mensaje = "El objeto se detuvo antes de llegar al final del plano."
            break

    # Asegurarse de añadir el punto final si no se alcanzó exactamente
    if x_actual < distancia_plano and len(posiciones) > 0:
        # Calcular el tiempo y velocidad para alcanzar exactamente la distancia_plano
        # x = x0 + v0*t + 0.5*a*t^2
        # 0.5*a*t^2 + v0*t + (x0-x) = 0
        A = 0.5 * aceleracion
        B = velocidades[-1] if velocidades else velocidad_inicial
        C = (posiciones[-1] if posiciones else 0) - distancia_plano

        if A == 0: # Movimiento rectilíneo uniforme
            if B != 0:
                dt_final = -C / B
            else:
                dt_final = 0 # No se mueve
        else:
            discriminante = B**2 - 4 * A * C
            if discriminante >= 0:
                t_sol1 = (-B + np.sqrt(discriminante)) / (2 * A)
                t_sol2 = (-B - np.sqrt(discriminante)) / (2 * A)
                dt_final = max(t_sol1, t_sol2) # Tomar el tiempo positivo
            else:
                dt_final = 0 # No hay solución real, no debería pasar si ya se movía

        if dt_final > 0:
            t_final = (tiempos_reales[-1] if tiempos_reales else 0) + dt_final
            x_final = distancia_plano
            v_final = (velocidades[-1] if velocidades else velocidad_inicial) + aceleracion * dt_final

            posiciones.append(x_final)
            velocidades.append(v_final)
            tiempos_reales.append(t_final)

    estado_animacion = []
    for i in range(len(tiempos_reales)):
        estado_animacion.append([tiempos_reales[i], posiciones[i], velocidades[i]])

    return {
        "tiempos": tiempos_reales,
        "posiciones": posiciones,
        "velocidades": velocidades,
        "aceleraciones": [aceleracion] * len(tiempos_reales),
        "mensaje": mensaje,
        "estado_animacion": estado_animacion
    }