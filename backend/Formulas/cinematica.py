import numpy as np
import math

GRAVEDAD = 9.81  # m/s^2

# --- Caída Libre ---

def calcular_tiempo_caida_libre(altura_inicial: float) -> float:
    """
    Calcula el tiempo que tarda un objeto en caer desde una altura inicial en caída libre.
    """
    if altura_inicial < 0:
        raise ValueError("La altura inicial no puede ser negativa.")
    if altura_inicial == 0:
        return 0.0
    return (2 * altura_inicial / GRAVEDAD)**0.5

def calcular_velocidad_final_caida_libre(altura_inicial: float) -> float:
    """
    Calcula la velocidad final de un objeto en caída libre desde una altura inicial.
    """
    if altura_inicial < 0:
        raise ValueError("La altura inicial no puede ser negativa.")
    return (2 * GRAVEDAD * altura_inicial)**0.5

def calcular_altura_caida_libre(tiempo: float, altura_inicial: float) -> float:
    """
    Calcula la altura de un objeto en caída libre en un tiempo dado.
    """
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    if altura_inicial < 0:
        raise ValueError("La altura inicial no puede ser negativa.")
    altura = altura_inicial - 0.5 * GRAVEDAD * tiempo**2
    return max(0.0, altura)

# --- Ecuaciones Cinemáticas ---

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
        t2 = (-b_cuadratica - math.sqrt(discriminante)) / (2 * a_cuadratica)
        
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

# --- Movimiento Armónico Simple ---

def calcular_periodo_frecuencia_mas(amplitud: float, frecuencia_angular: float) -> dict:
    """
    Calcula el período y la frecuencia de un objeto en Movimiento Armónico Simple.
    """
    if amplitud <= 0:
        raise ValueError("La amplitud debe ser positiva.")
    if frecuencia_angular <= 0:
        raise ValueError("La frecuencia angular (ω) debe ser positiva.")

    periodo = 2 * np.pi / frecuencia_angular
    frecuencia_hz = 1 / periodo

    return {"periodo": periodo, "frecuencia_hz": frecuencia_hz}

def calcular_posicion_mas(amplitud: float, frecuencia_angular: float, fase_inicial: float, tiempo: float) -> float:
    """
    Calcula la posición de un objeto en Movimiento Armónico Simple en un tiempo dado.
    x(t) = A * cos(ω*t + φ)
    """
    if amplitud <= 0:
        raise ValueError("La amplitud debe ser positiva.")
    if frecuencia_angular <= 0:
        raise ValueError("La frecuencia angular (ω) debe ser positiva.")
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")

    return amplitud * np.cos(frecuencia_angular * tiempo + fase_inicial)

def calcular_velocidad_mas(amplitud: float, frecuencia_angular: float, fase_inicial: float, tiempo: float) -> float:
    """
    Calcula la velocidad de un objeto en Movimiento Armónico Simple en un tiempo dado.
    v(t) = -Aω * sin(ω*t + φ)
    """
    if amplitud <= 0:
        raise ValueError("La amplitud debe ser positiva.")
    if frecuencia_angular <= 0:
        raise ValueError("La frecuencia angular (ω) debe ser positiva.")
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")

    return -amplitud * frecuencia_angular * np.sin(frecuencia_angular * tiempo + fase_inicial)

def calcular_aceleracion_mas(amplitud: float, frecuencia_angular: float, fase_inicial: float, tiempo: float) -> float:
    """
    Calcula la aceleración de un objeto en Movimiento Armónico Simple en un tiempo dado.
    a(t) = -Aω^2 * cos(ω*t + φ)
    """
    if amplitud <= 0:
        raise ValueError("La amplitud debe ser positiva.")
    if frecuencia_angular <= 0:
        raise ValueError("La frecuencia angular (ω) debe ser positiva.")
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")

    return -amplitud * (frecuencia_angular**2) * np.cos(frecuencia_angular * tiempo + fase_inicial)

# --- Movimiento Circular Uniforme ---

def calcular_periodo_mcu(velocidad_angular: float) -> float:
    """
    Calcula el período de un objeto en Movimiento Circular Uniforme.
    T = 2 * pi / omega
    """
    if velocidad_angular == 0:
        raise ValueError("La velocidad angular no puede ser cero para calcular el período.")
    return 2 * np.pi / abs(velocidad_angular)

def calcular_frecuencia_mcu(velocidad_angular: float) -> float:
    """
    Calcula la frecuencia de un objeto en Movimiento Circular Uniforme.
    f = omega / (2 * pi)
    """
    if velocidad_angular == 0:
        raise ValueError("La velocidad angular no puede ser cero para calcular la frecuencia.")
    return abs(velocidad_angular) / (2 * np.pi)

def calcular_velocidad_tangencial_mcu(radio: float, velocidad_angular: float) -> float:
    """
    Calcula la velocidad tangencial de un objeto en Movimiento Circular Uniforme.
    v = r * omega
    """
    if radio < 0:
        raise ValueError("El radio no puede ser negativo.")
    return radio * velocidad_angular

def calcular_aceleracion_centripeta_mcu(radio: float, velocidad_angular: float = None, velocidad_tangencial: float = None) -> float:
    """
    Calcula la aceleración centrípeta de un objeto en Movimiento Circular Uniforme.
    ac = v^2 / r = omega^2 * r
    """
    if radio <= 0:
        raise ValueError("El radio debe ser positivo para calcular la aceleración centrípeta.")
    
    if velocidad_angular is None and velocidad_tangencial is None:
        raise ValueError("Se debe proveer velocidad_angular o velocidad_tangencial.")
    
    if velocidad_angular is not None:
        return (velocidad_angular**2) * radio
    elif velocidad_tangencial is not None:
        return (velocidad_tangencial**2) / radio
    return 0.0 # Should not reach here

def calcular_posicion_angular_mcu(velocidad_angular: float, tiempo: float, angulo_inicial: float = 0.0) -> float:
    """
    Calcula la posición angular de un objeto en Movimiento Circular Uniforme en un tiempo dado.
    theta(t) = theta_0 + omega * t
    """
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    return angulo_inicial + velocidad_angular * tiempo

def calcular_posicion_lineal_mcu(radio: float, velocidad_angular: float, tiempo: float, angulo_inicial: float = 0.0) -> dict:
    """
    Calcula la posición lineal (x, y) de un objeto en Movimiento Circular Uniforme en un tiempo dado.
    x(t) = r * cos(theta(t))
    y(t) = r * sin(theta(t))
    """
    if radio < 0:
        raise ValueError("El radio no puede ser negativo.")
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    
    angulo_rad = calcular_posicion_angular_mcu(velocidad_angular, tiempo, angulo_inicial)
    posicion_x = radio * np.cos(angulo_rad)
    posicion_y = radio * np.sin(angulo_rad)
    return {"posicion_x": posicion_x, "posicion_y": posicion_y}

# --- MRU ---

def calcular_posicion_mru(posicion_inicial: float, velocidad: float, tiempo: float) -> float:
    """
    Calcula la posición final de un objeto en Movimiento Rectilíneo Uniforme (MRU).
    Fórmula: x(t) = x0 + v*t

    Args:
        posicion_inicial (float): Posición inicial del objeto (x0).
        velocidad (float): Velocidad constante del objeto (v).
        tiempo (float): Tiempo transcurrido (t).

    Returns:
        float: Posición final del objeto en el tiempo dado.
    Raises:
        ValueError: Si el tiempo es negativo.
    """
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    return posicion_inicial + velocidad * tiempo

# --- MRUV ---

def calcular_posicion_mruv(posicion_inicial: float, velocidad_inicial: float, aceleracion: float, tiempo: float) -> float:
    """
    Calcula la posición final de un objeto en Movimiento Rectilíneo Uniformemente Variado (MRUV).
    Fórmula: x(t) = x0 + v0*t + 0.5*a*t^2

    Args:
        posicion_inicial (float): Posición inicial del objeto (x0).
        velocidad_inicial (float): Velocidad inicial del objeto (v0).
        aceleracion (float): Aceleración constante del objeto (a).
        tiempo (float): Tiempo transcurrido (t).

    Returns:
        float: Posición final del objeto en el tiempo dado.
    Raises:
        ValueError: Si el tiempo es negativo.
    """
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    return posicion_inicial + velocidad_inicial * tiempo + 0.5 * aceleracion * tiempo**2

def calcular_velocidad_mruv(velocidad_inicial: float, aceleracion: float, tiempo: float) -> float:
    """
    Calcula la velocidad final de un objeto en Movimiento Rectilíneo Uniformemente Variado (MRUV).
    Fórmula: v(t) = v0 + a*t

    Args:
        velocidad_inicial (float): Velocidad inicial del objeto (v0).
        aceleracion (float): Aceleración constante del objeto (a).
        tiempo (float): Tiempo transcurrido (t).

    Returns:
        float: Velocidad final del objeto en el tiempo dado.
    Raises:
        ValueError: Si el tiempo es negativo.
    """
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    return velocidad_inicial + aceleracion * tiempo

# --- Péndulo ---

def calcular_periodo_pendulo(longitud: float) -> float:
    if longitud <= 0:
        raise ValueError("La longitud del péndulo debe ser positiva.")
    return 2 * np.pi * np.sqrt(longitud / GRAVEDAD)

def calcular_frecuencia_pendulo(longitud: float) -> float:
    if longitud <= 0:
        raise ValueError("La longitud del péndulo debe ser positiva.")
    return 1 / calcular_periodo_pendulo(longitud)

def calcular_posicion_angular_pendulo(longitud: float, angulo_inicial_grados: float, tiempo: float) -> float:
    if longitud <= 0:
        raise ValueError("La longitud del péndulo debe ser positiva.")
    angulo_inicial_rad = np.deg2rad(angulo_inicial_grados)
    frecuencia_angular = np.sqrt(GRAVEDAD / longitud)
    return angulo_inicial_rad * np.cos(frecuencia_angular * tiempo)

def calcular_velocidad_angular_pendulo(longitud: float, angulo_inicial_grados: float, tiempo: float) -> float:
    if longitud <= 0:
        raise ValueError("La longitud del péndulo debe ser positiva.")
    angulo_inicial_rad = np.deg2rad(angulo_inicial_grados)
    frecuencia_angular = np.sqrt(GRAVEDAD / longitud)
    return -angulo_inicial_rad * frecuencia_angular * np.sin(frecuencia_angular * tiempo)

def calcular_aceleracion_angular_pendulo(longitud: float, angulo_inicial_grados: float, tiempo: float) -> float:
    if longitud <= 0:
        raise ValueError("La longitud del péndulo debe ser positiva.")
    angulo_inicial_rad = np.deg2rad(angulo_inicial_grados)
    frecuencia_angular = np.sqrt(GRAVEDAD / longitud)
    return -angulo_inicial_rad * (frecuencia_angular**2) * np.cos(frecuencia_angular * tiempo)

# --- Tiro Parabólico ---

def calcular_componentes_velocidad_inicial(velocidad_inicial: float, angulo_lanzamiento_grados: float):
    angulo_lanzamiento_rad = np.deg2rad(angulo_lanzamiento_grados)
    vx0 = velocidad_inicial * np.cos(angulo_lanzamiento_rad)
    vy0 = velocidad_inicial * np.sin(angulo_lanzamiento_rad)
    return vx0, vy0

def calcular_tiempo_vuelo(velocidad_inicial: float, angulo_lanzamiento_grados: float, altura_inicial: float = 0.0):
    vy0 = velocidad_inicial * np.sin(np.deg2rad(angulo_lanzamiento_grados))
    discriminante = vy0**2 + 2 * GRAVEDAD * altura_inicial
    if discriminante < 0:
        return 0.0 # No debería ocurrir en un escenario físico real
    
    t1 = (vy0 + np.sqrt(discriminante)) / GRAVEDAD
    t2 = (vy0 - np.sqrt(discriminante)) / GRAVEDAD
    
    # El tiempo de vuelo es el valor positivo
    return max(t1, t2, 0.0)

def calcular_altura_maxima(velocidad_inicial: float, angulo_lanzamiento_grados: float, altura_inicial: float = 0.0):
    vy0 = velocidad_inicial * np.sin(np.deg2rad(angulo_lanzamiento_grados))
    h_max = altura_inicial + (vy0**2) / (2 * GRAVEDAD)
    return h_max

def calcular_alcance_horizontal(velocidad_inicial: float, angulo_lanzamiento_grados: float, altura_inicial: float = 0.0):
    vx0, _ = calcular_componentes_velocidad_inicial(velocidad_inicial, angulo_lanzamiento_grados)
    tiempo_vuelo = calcular_tiempo_vuelo(velocidad_inicial, angulo_lanzamiento_grados, altura_inicial)
    alcance = vx0 * tiempo_vuelo
    return alcance

def calcular_posicion_en_tiempo(velocidad_inicial: float, angulo_lanzamiento_grados: float, tiempo: float, altura_inicial: float = 0.0):
    vx0, vy0 = calcular_componentes_velocidad_inicial(velocidad_inicial, angulo_lanzamiento_grados)
    
    posicion_x = vx0 * tiempo
    posicion_y = altura_inicial + vy0 * tiempo - 0.5 * GRAVEDAD * tiempo**2
    
    return posicion_x, posicion_y

def calcular_velocidad_en_tiempo(velocidad_inicial: float, angulo_lanzamiento_grados: float, tiempo: float):
    vx0, vy0 = calcular_componentes_velocidad_inicial(velocidad_inicial, angulo_lanzamiento_grados)
    
    velocidad_x = vx0
    velocidad_y = vy0 - GRAVEDAD * tiempo
    
    velocidad_resultante = np.sqrt(velocidad_x**2 + velocidad_y**2)
    angulo_velocidad_rad = np.arctan2(velocidad_y, velocidad_x)
    angulo_velocidad_grados = np.rad2deg(angulo_velocidad_rad)
    
    return velocidad_x, velocidad_y, velocidad_resultante, angulo_velocidad_grados