import numpy as np

def simular_plano_inclinado_polea(
    masa1: float,
    masa2: float,
    angulo_inclinacion_grados: float,
    coeficiente_rozamiento_cinetico: float,
    tiempo_total_simulacion: float,
    num_puntos: int,
    gravedad: float = 9.81
):
    """
    Simula el movimiento de dos masas conectadas por una cuerda sobre una polea,
    donde una masa está en un plano inclinado con rozamiento y la otra cuelga verticalmente.

    Args:
        masa1 (float): Masa del objeto en el plano inclinado (kg).
        masa2 (float): Masa del objeto colgante (kg).
        angulo_inclinacion_grados (float): Ángulo del plano inclinado en grados.
        coeficiente_rozamiento_cinetico (float): Coeficiente de rozamiento cinético entre masa1 y el plano.
        tiempo_total_simulacion (float): Tiempo total de la simulación (s).
        num_puntos (int): Número de puntos de datos a generar para la simulación.
        gravedad (float): Aceleración debido a la gravedad (m/s^2).

    Returns:
        dict: Un diccionario con los resultados de la simulación, incluyendo:
              - 'parametros': Parámetros de entrada de la simulación.
              - 'estados_simulacion': Lista de diccionarios con el estado del sistema en cada instante de tiempo.
                Cada estado incluye 'tiempo', 'posicion_masa1', 'posicion_masa2', 'velocidad_masa1', 'velocidad_masa2',
                'aceleracion_masa1', 'aceleracion_masa2', 'tension'.
              - 'formulas_aplicadas': Descripción de las fórmulas y principios utilizados.
    """

    angulo_rad = np.radians(angulo_inclinacion_grados)

    # Ecuaciones de movimiento (considerando masa1 subiendo o bajando el plano)
    # Suma de fuerzas para masa1 (eje x a lo largo del plano):
    # T - m1*g*sin(theta) - f_rozamiento = m1*a
    # Suma de fuerzas para masa2 (eje y vertical):
    # m2*g - T = m2*a
    # f_rozamiento = mu_k * N = mu_k * m1*g*cos(theta)

    # Despejando la aceleración 'a' del sistema:
    # T = m1*a + m1*g*sin(theta) + mu_k*m1*g*cos(theta) (si masa1 sube)
    # T = m1*a + m1*g*sin(theta) - mu_k*m1*g*cos(theta) (si masa1 baja)
    # Reemplazando T en la segunda ecuación:
    # m2*g - (m1*a + m1*g*sin(theta) + mu_k*m1*g*cos(theta)) = m2*a
    # m2*g - m1*g*sin(theta) - mu_k*m1*g*cos(theta) = (m1 + m2)*a

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
    direccion_movimiento = 0 # 0: no movimiento, 1: masa1 sube, -1: masa1 baja

    if fuerza_neta_potencial_arriba > 0:
        # Masa2 tira de masa1 hacia arriba del plano
        aceleracion = fuerza_neta_potencial_arriba / (masa1 + masa2)
        direccion_movimiento = 1
    elif fuerza_neta_potencial_abajo > 0:
        # Masa1 se desliza hacia abajo del plano
        aceleracion = fuerza_neta_potencial_abajo / (masa1 + masa2)
        direccion_movimiento = -1
    else:
        # El sistema está en equilibrio o la fuerza neta es cero
        aceleracion = 0.0
        tension = masa2 * gravedad # Si no hay movimiento, la tensión equilibra el peso de masa2
        if masa1 * gravedad * np.sin(angulo_rad) > masa2 * gravedad:
            tension = masa1 * gravedad * np.sin(angulo_rad) - coeficiente_rozamiento_cinetico * masa1 * gravedad * np.cos(angulo_rad)
        else:
            tension = masa2 * gravedad


    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    estados_simulacion = []

    posicion_inicial_masa1 = 0.0
    posicion_inicial_masa2 = 0.0
    velocidad_inicial = 0.0

    for i, t in enumerate(tiempos):
        if i == 0:
            posicion_masa1 = posicion_inicial_masa1
            posicion_masa2 = posicion_inicial_masa2
            velocidad_masa1 = velocidad_inicial
            velocidad_masa2 = velocidad_inicial
        else:
            dt = tiempos[i] - tiempos[i-1]
            velocidad_masa1 = velocidad_inicial + aceleracion * t * direccion_movimiento
            velocidad_masa2 = velocidad_inicial + aceleracion * t * direccion_movimiento
            posicion_masa1 = posicion_inicial_masa1 + velocidad_inicial * t * direccion_movimiento + 0.5 * aceleracion * t**2 * direccion_movimiento
            posicion_masa2 = posicion_inicial_masa2 + velocidad_inicial * t * direccion_movimiento + 0.5 * aceleracion * t**2 * direccion_movimiento

        # Calcular la tensión en cada instante (si hay movimiento)
        if direccion_movimiento == 1:
            tension = masa2 * gravedad - masa2 * aceleracion
        elif direccion_movimiento == -1:
            tension = masa2 * gravedad + masa2 * aceleracion # Tensión es mayor si masa2 acelera hacia arriba
        else:
            # Si no hay movimiento, la tensión equilibra las fuerzas
            tension = masa2 * gravedad

        estados_simulacion.append({
            'tiempo': t,
            'posicion_masa1': posicion_masa1,
            'posicion_masa2': posicion_masa2,
            'velocidad_masa1': velocidad_masa1,
            'velocidad_masa2': velocidad_masa2,
            'aceleracion_masa1': aceleracion * direccion_movimiento,
            'aceleracion_masa2': aceleracion * direccion_movimiento,
            'tension': tension
        })

    formulas_aplicadas = [
        "Segunda Ley de Newton: ΣF = ma",
        "Fuerza de Rozamiento Cinético: f_k = μ_k * N",
        "Componentes de la gravedad en un plano inclinado: mg*sin(θ) y mg*cos(θ)",
        "Ecuaciones de cinemática para movimiento uniformemente acelerado: v = v₀ + at, x = x₀ + v₀t + ½at²"
    ]

    return {
        'parametros': {
            'masa1': masa1,
            'masa2': masa2,
            'angulo_inclinacion_grados': angulo_inclinacion_grados,
            'coeficiente_rozamiento_cinetico': coeficiente_rozamiento_cinetico,
            'tiempo_total_simulacion': tiempo_total_simulacion,
            'num_puntos': num_puntos,
            'gravedad': gravedad
        },
        'estados_simulacion': estados_simulacion,
        'formulas_aplicadas': formulas_aplicadas
    }