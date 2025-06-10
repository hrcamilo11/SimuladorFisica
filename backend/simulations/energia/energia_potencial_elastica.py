import numpy as np

def calcular_energia_potencial_elastica(masa, constante_elastica, amplitud, tiempo_total, num_puntos=100, fase_inicial_rad=0):
    """
    Calcula la energía potencial elástica, cinética y mecánica total para un sistema masa-resorte en MAS.
    U_elastica = 0.5 * k * x^2 (Energía Potencial Elástica)
    K = 0.5 * m * v^2 (Energía Cinética)
    E_mecanica = U_elastica + K = constante (en ausencia de fricción)
    x(t) = A * cos(ω*t + φ)
    v(t) = -A * ω * sin(ω*t + φ)
    ω = sqrt(k/m) (frecuencia angular)
    """
    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")
    if constante_elastica <= 0:
        raise ValueError("La constante elástica debe ser positiva.")
    if amplitud < 0:
        raise ValueError("La amplitud no puede ser negativa.") # Amplitud es una magnitud
    if tiempo_total < 0:
        raise ValueError("El tiempo total no puede ser negativo.")
    if num_puntos < 2 and tiempo_total > 0:
        num_puntos = 2
    elif num_puntos < 1:
        num_puntos = 1
    
    omega = np.sqrt(constante_elastica / masa)
    if tiempo_total == 0: # Si el tiempo es cero, solo un punto en el estado inicial
        num_puntos = 1
        
    tiempos = np.linspace(0, tiempo_total, num_puntos)
    
    posiciones = amplitud * np.cos(omega * tiempos + fase_inicial_rad)
    velocidades = -amplitud * omega * np.sin(omega * tiempos + fase_inicial_rad)
    
    energia_potencial_elastica = 0.5 * constante_elastica * posiciones**2
    energia_cinetica = 0.5 * masa * velocidades**2
    energia_mecanica_total = energia_potencial_elastica + energia_cinetica
    
    periodo = 2 * np.pi / omega if omega > 0 else float('inf')
    frecuencia = omega / (2 * np.pi) if omega > 0 else 0

    estado_animacion = {
        "tiempos": list(tiempos),
        "posiciones": list(posiciones),
        "velocidades": list(velocidades),
        "energia_potencial_elastica": list(energia_potencial_elastica),
        "energia_cinetica": list(energia_cinetica),
        "energia_mecanica_total": list(energia_mecanica_total)
    }

    return {
        "periodo": periodo,
        "frecuencia": frecuencia,
        "omega": omega,
        "estado_animacion": estado_animacion
    }

def simular_energia_potencial_elastica(masa, constante_elastica, amplitud, tiempo_total, num_puntos=100, fase_inicial_rad=0):
    """
    Función API para simular el cálculo de la energía potencial elástica.
    """
    try:
        resultados = calcular_energia_potencial_elastica(masa, constante_elastica, amplitud, tiempo_total, num_puntos, fase_inicial_rad)
        return {
            "success": True,
            "message": "Cálculo de energía potencial elástica exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }