import math

def calcular_campo_magnetico(corriente, distancia, permeabilidad_vacio=4 * math.pi * (10**-7)):
    """
    Calcula el campo magnético (B) producido por un conductor largo y recto.

    Args:
        corriente (float): La corriente en amperios (A).
        distancia (float): La distancia perpendicular al conductor en metros (m).
        permeabilidad_vacio (float): La permeabilidad magnética del vacío (μ0).

    Returns:
        dict: Un diccionario con el campo magnético y el estado para animación.

    Raises:
        ValueError: Si la distancia es cero.
    """
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    campo_magnetico = (permeabilidad_vacio * corriente) / (2 * math.pi * distancia)
    estado_animacion = {"corriente": corriente, "distancia": distancia, "campo_magnetico": campo_magnetico}
    return {"campo_magnetico": campo_magnetico, "estado_animacion": estado_animacion}

def simular_campo_magnetico(corriente, distancia, permeabilidad_vacio=4 * math.pi * (10**-7)):
    """
    Función API para simular el cálculo del campo magnético.
    """
    try:
        resultados = calcular_campo_magnetico(corriente, distancia, permeabilidad_vacio)
        return {
            "success": True,
            "message": "Cálculo de campo magnético exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_fuerza_lorentz(carga, velocidad, campo_magnetico, angulo_grados):
    """
    Calcula la fuerza de Lorentz (F) sobre una partícula cargada en un campo magnético.

    Args:
        carga (float): La carga de la partícula en culombios (C).
        velocidad (float): La velocidad de la partícula en metros por segundo (m/s).
        campo_magnetico (float): La magnitud del campo magnético en teslas (T).
        angulo_grados (float): El ángulo entre la velocidad y el campo magnético en grados.

    Returns:
        dict: Un diccionario con la fuerza de Lorentz y el estado para animación.
    """
    angulo_radianes = math.radians(angulo_grados)
    fuerza_lorentz = carga * velocidad * campo_magnetico * math.sin(angulo_radianes)
    estado_animacion = {"carga": carga, "velocidad": velocidad, "campo_magnetico": campo_magnetico, "angulo_grados": angulo_grados, "fuerza_lorentz": fuerza_lorentz}
    return {"fuerza_lorentz": fuerza_lorentz, "estado_animacion": estado_animacion}

def simular_fuerza_lorentz(carga, velocidad, campo_magnetico, angulo_grados):
    """
    Función API para simular el cálculo de la fuerza de Lorentz.
    """
    try:
        resultados = calcular_fuerza_lorentz(carga, velocidad, campo_magnetico, angulo_grados)
        return {
            "success": True,
            "message": "Cálculo de fuerza de Lorentz exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_flujo_magnetico(campo_magnetico, area, angulo_grados):
    """
    Calcula el flujo magnético (Φ) a través de una superficie.

    Args:
        campo_magnetico (float): La magnitud del campo magnético en teslas (T).
        area (float): El área de la superficie en metros cuadrados (m²).
        angulo_grados (float): El ángulo entre el vector normal al área y el campo magnético en grados.

    Returns:
        dict: Un diccionario con el flujo magnético y el estado para animación.
    """
    angulo_radianes = math.radians(angulo_grados)
    flujo_magnetico = campo_magnetico * area * math.cos(angulo_radianes)
    estado_animacion = {"campo_magnetico": campo_magnetico, "area": area, "angulo_grados": angulo_grados, "flujo_magnetico": flujo_magnetico}
    return {"flujo_magnetico": flujo_magnetico, "estado_animacion": estado_animacion}

def simular_flujo_magnetico(campo_magnetico, area, angulo_grados):
    """
    Función API para simular el cálculo del flujo magnético.
    """
    try:
        resultados = calcular_flujo_magnetico(campo_magnetico, area, angulo_grados)
        return {
            "success": True,
            "message": "Cálculo de flujo magnético exitoso.",
            "resultados": resultados
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }

def calcular_ley_faraday(cambio_flujo_magnetico, cambio_tiempo, numero_espiras=1):
    """
    Calcula la fuerza electromotriz (FEM) inducida según la Ley de Faraday.

    Args:
        cambio_flujo_magnetico (float): El cambio en el flujo magnético en webers (Wb).
        cambio_tiempo (float): El cambio en el tiempo en segundos (s).
        numero_espiras (int): El número de espiras en la bobina.

    Returns:
        dict: Un diccionario con la fuerza electromotriz y el estado para animación.

    Raises:
        ValueError: Si el cambio de tiempo es cero.
    """
    if cambio_tiempo == 0:
        raise ValueError("El cambio en el tiempo no puede ser cero.")
    fem = -numero_espiras * (cambio_flujo_magnetico / cambio_tiempo)
    estado_animacion = {"cambio_flujo_magnetico": cambio_flujo_magnetico, "cambio_tiempo": cambio_tiempo, "numero_espiras": numero_espiras, "fem": fem}
    return {"fem": fem, "estado_animacion": estado_animacion}

def simular_ley_faraday(cambio_flujo_magnetico, cambio_tiempo, numero_espiras=1):
    """
    Función API para simular el cálculo de la Ley de Faraday.
    """
    try:
        resultados = calcular_ley_faraday(cambio_flujo_magnetico, cambio_tiempo, numero_espiras)
        return {
            "success": True,
            "message": "Cálculo de Ley de Faraday exitoso.",
            "resultados": resultados
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "resultados": None
        }