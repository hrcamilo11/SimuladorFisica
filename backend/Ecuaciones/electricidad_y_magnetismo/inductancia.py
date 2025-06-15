def calcular_inductancia(flujo_magnetico, corriente, numero_espiras):
    """
    Calcula la inductancia (L) de una bobina.

    Args:
        flujo_magnetico (float): El flujo magnético en webers (Wb).
        corriente (float): La corriente en amperios (A).
        numero_espiras (int): El número de espiras en la bobina.

    Returns:
        dict: Un diccionario con la inductancia y el estado para animación.

    Raises:
        ValueError: Si la corriente es cero.
    """
    if corriente == 0:
        raise ValueError("La corriente no puede ser cero.")
    inductancia = (numero_espiras * flujo_magnetico) / corriente
    estado_animacion = {"flujo_magnetico": flujo_magnetico, "corriente": corriente, "numero_espiras": numero_espiras, "inductancia": inductancia}
    return {"inductancia": inductancia, "estado_animacion": estado_animacion}

def calcular_energia_inductor(inductancia, corriente):
    """
    Calcula la energía almacenada (U) en un inductor.

    Args:
        inductancia (float): La inductancia en henrios (H).
        corriente (float): La corriente en amperios (A).

    Returns:
        dict: Un diccionario con la energía y el estado para animación.
    """
    energia = 0.5 * inductancia * (corriente ** 2)
    estado_animacion = {"inductancia": inductancia, "corriente": corriente, "energia": energia}
    return {"energia": energia, "estado_animacion": estado_animacion}