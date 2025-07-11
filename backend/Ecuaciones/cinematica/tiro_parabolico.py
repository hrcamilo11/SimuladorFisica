import numpy as np
from backend.Ecuaciones.cinematica.ecuaciones_cinematica import calcular_posicion_final_tiempo

GRAVEDAD = 9.81  # m/s^2

def calcular_tiro_parabolico(velocidad_inicial, angulo_lanzamiento_grados, altura_inicial=0, num_puntos=100):
    """
    Calcula la trayectoria de un proyectil.
    Retorna tiempos, posiciones_x, posiciones_y.
    """
    if velocidad_inicial <= 0:
        return [], [], []
        
    angulo_lanzamiento_rad = np.deg2rad(angulo_lanzamiento_grados)

    # Ajustar para ángulos cercanos a 0, 90, 180 grados para evitar problemas de punto flotante
    if abs(angulo_lanzamiento_grados) < 1e-6 or abs(angulo_lanzamiento_grados - 180) < 1e-6: # Horizontal
        v0x = velocidad_inicial * np.cos(angulo_lanzamiento_rad)
        v0y = 0.0
    elif abs(angulo_lanzamiento_grados - 90) < 1e-6: # Vertical
        v0x = 0.0
        v0y = velocidad_inicial * np.sin(angulo_lanzamiento_rad)
    else:
        v0x = velocidad_inicial * np.cos(angulo_lanzamiento_rad)
        v0y = velocidad_inicial * np.sin(angulo_lanzamiento_rad)

    # Tiempo total de vuelo (hasta que y vuelva a ser altura_inicial o 0 si altura_inicial es 0)
    # y(t) = y0 + v0y*t - 0.5*g*t^2
    # Si y0 = 0, t_vuelo = 2*v0y/g
    # Si y0 > 0, resolvemos 0 = y0 + v0y*t - 0.5*g*t^2 para t (ecuación cuadrática)
    # at^2 + bt + c = 0  => a = -0.5g, b = v0y, c = y0
    # t = [-b +/- sqrt(b^2 - 4ac)] / 2a
    a = -0.5 * GRAVEDAD
    b = v0y
    c = altura_inicial
    
    discriminante = b**2 - 4*a*c
    if discriminante < 0: # No alcanza el suelo si se lanza hacia arriba desde altura y no tiene suficiente v0y
        # En este caso, calculamos hasta el punto más alto y un poco más
        tiempo_max_altura = v0y / GRAVEDAD
        if tiempo_max_altura <=0: #Lanzado hacia abajo
            tiempo_hasta_suelo_directo = np.sqrt(2 * altura_inicial / GRAVEDAD) if v0y == 0 else (-v0y - np.sqrt(v0y**2 - 4*a*c))/(2*a)
            tiempo_total_simulacion = tiempo_hasta_suelo_directo if tiempo_hasta_suelo_directo > 0 else 1 # fallback
        else:
            tiempo_total_simulacion = tiempo_max_altura * 2 # Estimación simple
    else:
        t1 = (-b + np.sqrt(discriminante)) / (2*a)
        t2 = (-b - np.sqrt(discriminante)) / (2*a)
        tiempo_total_simulacion = max(t1, t2)
        if tiempo_total_simulacion <= 0: # Si el tiempo es negativo o cero, algo anda mal o ya está en el suelo
             # Podría ser que se lanza hacia abajo desde y0. t_vuelo es el positivo.
             tiempo_total_simulacion = t2 if t2 > 0 else (t1 if t1 > 0 else 1) # fallback

    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    posiciones_x = [calcular_posicion_final_tiempo(0, v0x, 0, t) for t in tiempos]
    posiciones_y = [calcular_posicion_final_tiempo(altura_inicial, v0y, -GRAVEDAD, t) for t in tiempos]

    # Filtrar puntos después de tocar el suelo (y < 0)
    tiempos_reales = []
    x_reales = []
    y_reales = []
    for t, x, y_pos in zip(tiempos, posiciones_x, posiciones_y):
        if y_pos >= 0:
            tiempos_reales.append(t)
            x_reales.append(x)
            y_reales.append(y_pos)
        else:
            # Interpolar para el punto de impacto exacto
            if not y_reales or y_reales[-1] > 0:
                # y_prev + v0y_prev * dt - 0.5 * g * dt^2 = 0 ... complejo
                # Simplificación: añadir el punto de impacto (y=0)
                # Necesitamos recalcular t para y=0 usando la fórmula cuadrática completa desde el inicio
                # Esto ya se hizo para tiempo_total_simulacion, así que usamos ese tiempo si es el correcto
                if tiempo_total_simulacion > (tiempos_reales[-1] if tiempos_reales else 0):
                    x_impacto = calcular_posicion_final_tiempo(0, v0x, 0, tiempo_total_simulacion)
                    tiempos_reales.append(tiempo_total_simulacion)
                    x_reales.append(x_impacto)
                    y_reales.append(0)
            break
            
    # Combinar los estados en una lista de diccionarios para facilitar la animación
    estados_simulacion = [
        {"tiempo": t, "posicion_x": x, "posicion_y": y}
        for t, x, y in zip(tiempos_reales, x_reales, y_reales)
    ]

    return tiempos_reales, x_reales, y_reales, tiempo_total_simulacion, estados_simulacion