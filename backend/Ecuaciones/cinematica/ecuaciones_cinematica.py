import math

def calcular_velocidad_final_tiempo(velocidad_inicial: float, aceleracion: float, tiempo: float) -> float:
    """
    Calcula la velocidad final usando: v = v0 + at
    """
    return velocidad_inicial + aceleracion * tiempo

def calcular_posicion_final_tiempo(posicion_inicial: float, velocidad_inicial: float, aceleracion: float, tiempo: float) -> float:
    """
    Calcula la posición final usando: x = x0 + v0*t + 0.5*a*t^2
    """
    return posicion_inicial + velocidad_inicial * tiempo + 0.5 * aceleracion * tiempo**2

def calcular_velocidad_final_desplazamiento(velocidad_inicial: float, aceleracion: float, desplazamiento: float) -> float:
    """
    Calcula la velocidad final usando: v^2 = v0^2 + 2*a*dx
    Retorna la velocidad final (puede ser positiva o negativa) o None si no es posible.
    """
    discriminante = velocidad_inicial**2 + 2 * aceleracion * desplazamiento
    if discriminante < 0:
        return None # No hay solución real
    return math.sqrt(discriminante) # Se asume la raíz positiva, el contexto determinará si es + o -

def calcular_desplazamiento_velocidades(velocidad_inicial: float, velocidad_final: float, tiempo: float) -> float:
    """
    Calcula el desplazamiento usando: dx = 0.5 * (v0 + v) * t
    """
    return 0.5 * (velocidad_inicial + velocidad_final) * tiempo

def calcular_tiempo_desplazamiento_velocidades(posicion_inicial: float, posicion_final: float, velocidad_inicial: float, velocidad_final: float) -> float:
    """
    Calcula el tiempo usando: t = 2 * (x - x0) / (v0 + v)
    """
    if (velocidad_inicial + velocidad_final) == 0:
        return None # Evitar división por cero
    return 2 * (posicion_final - posicion_inicial) / (velocidad_inicial + velocidad_final)

def calcular_aceleracion_velocidades_tiempo(velocidad_inicial: float, velocidad_final: float, tiempo: float) -> float:
    """
    Calcula la aceleración usando: a = (v - v0) / t
    """
    if tiempo == 0:
        return None # Evitar división por cero
    return (velocidad_final - velocidad_inicial) / tiempo

def calcular_tiempo_posicion_velocidad_aceleracion(posicion_inicial: float, velocidad_inicial: float, aceleracion: float, posicion_final: float) -> tuple[float, float] | float | None:
    """
    Calcula el tiempo usando: x = x0 + v0*t + 0.5*a*t^2 (ecuación cuadrática)
    Retorna una tupla de dos tiempos si hay dos soluciones, un solo tiempo si hay una, o None si no hay soluciones reales.
    """
    a_cuadratica = 0.5 * aceleracion
    b_cuadratica = velocidad_inicial
    c_cuadratica = posicion_inicial - posicion_final

    if a_cuadratica == 0:
        if b_cuadratica == 0:
            return None # No es una ecuación válida para t
        else:
            return -c_cuadratica / b_cuadratica # Ecuación lineal

    discriminante = b_cuadratica**2 - 4 * a_cuadratica * c_cuadratica

    if discriminante < 0:
        return None # No hay soluciones reales
    elif discriminante == 0:
        t = -b_cuadratica / (2 * a_cuadratica)
        return t if t >= 0 else None # Solo soluciones de tiempo positivo
    else:
        t1 = (-b_cuadratica + math.sqrt(discriminante)) / (2 * a_cuadratica)
        t2 = (-b_cuadratica - math.cuadratica.sqrt(discriminante)) / (2 * a_cuadratica)
        
        soluciones = []
        if t1 >= 0: soluciones.append(t1)
        if t2 >= 0: soluciones.append(t2)
        
        if len(soluciones) == 2: return tuple(soluciones)
        if len(soluciones) == 1: return soluciones[0]
        return None

def calcular_aceleracion_posicion_velocidad_tiempo(posicion_inicial: float, posicion_final: float, velocidad_inicial: float, tiempo: float) -> float | None:
    """
    Calcula la aceleración usando: a = 2 * (x - x0 - v0*t) / t^2
    """
    if tiempo == 0:
        return None # Evitar división por cero
    return 2 * (posicion_final - posicion_inicial - velocidad_inicial * tiempo) / (tiempo**2)

def calcular_posicion_final_velocidad_aceleracion(posicion_inicial: float, velocidad_inicial: float, velocidad_final: float, aceleracion: float) -> float | None:
    """
    Calcula la posición final usando: x = x0 + (v^2 - v0^2) / (2*a)
    """
    if aceleracion == 0:
        return None # Si la aceleración es cero, esta ecuación no es adecuada
    return posicion_inicial + (velocidad_final**2 - velocidad_inicial**2) / (2 * aceleracion)