import math

def calcular_resistencia_total_serie(resistencias: list[float]) -> float:
    """
    Calcula la resistencia total de resistencias en serie.

    Args:
        resistencias (list): Una lista de valores de resistencia en ohmios (Ω).

    Returns:
        float: La resistencia total en ohmios (Ω).
    """
    return sum(resistencias)

def calcular_resistencia_total_paralelo(resistencias: list[float]) -> float:
    """
    Calcula la resistencia total de resistencias en paralelo.

    Args:
        resistencias (list): Una lista de valores de resistencia en ohmios (Ω).

    Returns:
        float: La resistencia total en ohmios (Ω).
    Raises:
        ValueError: Si alguna resistencia es cero, lo que resultaría en una división por cero.
    """
    if 0 in resistencias:
        raise ValueError("No se puede calcular la resistencia en paralelo si alguna resistencia es cero.")
    return 1 / sum(1/r for r in resistencias)

def calcular_corriente_total(voltaje_total: float, resistencia_total: float) -> float:
    """
    Calcula la corriente total en un circuito usando la Ley de Ohm.

    Args:
        voltaje_total (float): El voltaje total en voltios (V).
        resistencia_total (float): La resistencia total en ohmios (Ω).

    Returns:
        float: La corriente total en amperios (A).
    Raises:
        ValueError: Si la resistencia total es cero.
    """
    if resistencia_total == 0:
        raise ValueError("La resistencia total no puede ser cero.")
    return voltaje_total / resistencia_total

def calcular_voltaje_resistor(corriente: float, resistencia: float) -> float:
    """
    Calcula el voltaje a través de un resistor usando la Ley de Ohm.

    Args:
        corriente (float): La corriente que pasa por el resistor en amperios (A).
        resistencia (float): La resistencia del resistor en ohmios (Ω).

    Returns:
        float: El voltaje a través del resistor en voltios (V).
    """
    return corriente * resistencia

def calcular_potencia_disipada_resistor(corriente: float, resistencia: float) -> float:
    """
    Calcula la potencia disipada por un resistor.

    Args:
        corriente (float): La corriente que pasa por el resistor en amperios (A).
        resistencia (float): La resistencia del resistor en ohmios (Ω).

    Returns:
        float: La potencia disipada en vatios (W).
    """
    return corriente**2 * resistencia

def calcular_resistencia_equivalente_serie(resistencias: list[float]) -> float:
    """
    Calcula la resistencia equivalente de un conjunto de resistencias en serie.

    Args:
        resistencias (list): Una lista de resistencias en ohmios (Ω).

    Returns:
        float: La resistencia equivalente en ohmios (Ω).
    """
    return sum(resistencias)

def calcular_campo_electrico_carga_puntual(carga: float, distancia: float, k: float = 8.9875e9) -> float:
    """
    Calcula el campo eléctrico (E) producido por una carga puntual.

    Args:
        carga (float): La magnitud de la carga en culombios (C).
        distancia (float): La distancia desde la carga en metros (m).
        k (float): La constante de Coulomb (N·m²/C²).

    Returns:
        float: El campo eléctrico en newtons por culombio (N/C).

    Raises:
        ValueError: Si la distancia es cero.
    """
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    campo_electrico = (k * abs(carga)) / (distancia**2)
    return campo_electrico

def calcular_fuerza_electrica_campo(carga_prueba: float, campo_electrico: float) -> float:
    """
    Calcula la fuerza eléctrica (F) sobre una carga de prueba en un campo eléctrico.

    Args:
        carga_prueba (float): La magnitud de la carga de prueba en culombios (C).
        campo_electrico (float): La magnitud del campo eléctrico en newtons por culombio (N/C).

    Returns:
        float: La fuerza eléctrica en newtons (N).
    """
    fuerza_electrica = carga_prueba * campo_electrico
    return fuerza_electrica

def calcular_campo_magnetico_solenoide(permeabilidad_vacio: float, numero_espiras: float, corriente: float, longitud: float) -> float:
    """
    Calcula el campo magnético (B) dentro de un solenoide.

    Args:
        permeabilidad_vacio (float): Permeabilidad magnética del vacío (μ₀).
        numero_espiras (float): Número de espiras del solenoide.
        corriente (float): Corriente que fluye a través del solenoide en amperios (A).
        longitud (float): Longitud del solenoide en metros (m).

    Returns:
        float: Campo magnético en teslas (T).

    Raises:
        ValueError: Si la longitud del solenoide es cero.
    """
    if longitud == 0:
        raise ValueError("La longitud del solenoide no puede ser cero.")
    campo_magnetico = (permeabilidad_vacio * numero_espiras * corriente) / longitud
    return campo_magnetico

def calcular_capacitancia(carga: float, voltaje: float) -> float:
    """
    Calcula la capacitancia (C) de un capacitor.

    Args:
        carga (float): La carga almacenada en el capacitor en culombios (C).
        voltaje (float): El voltaje a través del capacitor en voltios (V).

    Returns:
        float: La capacitancia en faradios (F).

    Raises:
        ValueError: Si el voltaje es cero.
    """
    if voltaje == 0:
        raise ValueError("El voltaje no puede ser cero.")
    capacitancia = carga / voltaje
    return capacitancia

def calcular_carga_capacitor(capacitancia: float, voltaje: float) -> float:
    """
    Calcula la carga (Q) almacenada en un capacitor.

    Args:
        capacitancia (float): La capacitancia del capacitor en faradios (F).
        voltaje (float): El voltaje a través del capacitor en voltios (V).

    Returns:
        float: La carga en culombios (C).
    """
    carga = capacitancia * voltaje
    return carga

def calcular_voltaje_capacitor(carga: float, capacitancia: float) -> float:
    """
    Calcula el voltaje (V) a través de un capacitor.

    Args:
        carga (float): La carga almacenada en el capacitor en culombios (C).
        capacitancia (float): La capacitancia del capacitor en faradios (F).

    Returns:
        float: El voltaje en voltios (V).

    Raises:
        ValueError: Si la capacitancia es cero.
    """
    if capacitancia == 0:
        raise ValueError("La capacitancia no puede ser cero.")
    voltaje = carga / capacitancia
    return voltaje

def calcular_energia_capacitor(capacitancia: float, voltaje: float) -> float:
    """
    Calcula la energía (U) almacenada en un capacitor.

    Args:
        capacitancia (float): La capacitancia del capacitor en faradios (F).
        voltaje (float): El voltaje a través del capacitor en voltios (V).

    Returns:
        float: La energía en julios (J).
    """
    energia = 0.5 * capacitancia * (voltaje**2)
    return energia

def calcular_fuerza_entre_conductores(permeabilidad_vacio: float, corriente1: float, corriente2: float, longitud: float, distancia: float) -> float:
    """
    Calcula la fuerza entre dos conductores paralelos que transportan corriente.

    Args:
        permeabilidad_vacio (float): Permeabilidad magnética del vacío (μ₀).
        corriente1 (float): Corriente en el primer conductor en amperios (A).
        corriente2 (float): Corriente en el segundo conductor en amperios (A).
        longitud (float): Longitud de los conductores en metros (m).
        distancia (float): Distancia entre los conductores en metros (m).

    Returns:
        float: La fuerza en newtons (N).

    Raises:
        ValueError: Si la distancia es cero.
    """
    if distancia == 0:
        raise ValueError("La distancia entre los conductores no puede ser cero.")
    fuerza = (permeabilidad_vacio * corriente1 * corriente2 * longitud) / (2 * math.pi * distancia)
    return fuerza

def calcular_inductancia(flujo_magnetico: float, corriente: float, numero_espiras: int = 1) -> float:
    """
    Calcula la inductancia (L) de una bobina.

    Args:
        flujo_magnetico (float): El flujo magnético a través de la bobina en webers (Wb).
        corriente (float): La corriente que pasa por la bobina en amperios (A).
        numero_espiras (int): El número de espiras en la bobina.

    Returns:
        float: La inductancia en henrios (H).

    Raises:
        ValueError: Si la corriente es cero.
    """
    if corriente == 0:
        raise ValueError("La corriente no puede ser cero.")
    inductancia = (numero_espiras * flujo_magnetico) / corriente
    return inductancia

def calcular_energia_inductor(inductancia: float, corriente: float) -> float:
    """
    Calcula la energía (U) almacenada en un inductor.

    Args:
        inductancia (float): La inductancia del inductor en henrios (H).
        corriente (float): La corriente que pasa por el inductor en amperios (A).

    Returns:
        float: La energía en julios (J).
    """
    energia = 0.5 * inductancia * (corriente**2)
    return energia

def calcular_fuerza_coulomb(carga1: float, carga2: float, distancia: float, k: float = 8.9875e9) -> float:
    """
    Calcula la fuerza eléctrica entre dos cargas puntuales utilizando la Ley de Coulomb.

    Args:
        carga1 (float): La magnitud de la primera carga en culombios (C).
        carga2 (float): La magnitud de la segunda carga en culombios (C).
        distancia (float): La distancia entre las cargas en metros (m).
        k (float): La constante de Coulomb (N·m²/C²).

    Returns:
        float: La fuerza eléctrica en newtons (N).

    Raises:
        ValueError: Si la distancia es cero.
    """
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    fuerza = (k * carga1 * carga2) / (distancia**2)
    return fuerza

def calcular_ley_ohm(valor1: float, valor2: float, tipo_calculo: str) -> float:
    """
    Calcula el voltaje, la corriente o la resistencia utilizando la Ley de Ohm.

    Args:
        valor1 (float): Primer valor (depende del tipo de cálculo).
        valor2 (float): Segundo valor (depende del tipo de cálculo).
        tipo_calculo (str): El tipo de cálculo a realizar ('voltaje', 'corriente', 'resistencia').

    Returns:
        float: El resultado del cálculo.

    Raises:
        ValueError: Si el tipo de cálculo no es válido o si se intenta dividir por cero.
    """
    if tipo_calculo == 'voltaje':
        # valor1 = corriente, valor2 = resistencia
        return valor1 * valor2
    elif tipo_calculo == 'corriente':
        # valor1 = voltaje, valor2 = resistencia
        if valor2 == 0:
            raise ValueError("La resistencia no puede ser cero para calcular la corriente.")
        return valor1 / valor2
    elif tipo_calculo == 'resistencia':
        # valor1 = voltaje, valor2 = corriente
        if valor2 == 0:
            raise ValueError("La corriente no puede ser cero para calcular la resistencia.")
        return valor1 / valor2
    else:
        raise ValueError("Tipo de cálculo no válido. Use 'voltaje', 'corriente' o 'resistencia'.")

def calcular_potencia_ohm(voltaje: float = None, corriente: float = None, resistencia: float = None) -> float:
    """
    Calcula la potencia eléctrica utilizando la Ley de Ohm (P = V*I, P = I^2*R, P = V^2/R).

    Args:
        voltaje (float, optional): El voltaje en voltios (V).
        corriente (float, optional): La corriente en amperios (A).
        resistencia (float, optional): La resistencia en ohmios (Ω).

    Returns:
        float: La potencia eléctrica en vatios (W).

    Raises:
        ValueError: Si no se proporcionan suficientes parámetros o si se intenta dividir por cero.
    """
    if voltaje is not None and corriente is not None:
        return voltaje * corriente
    elif corriente is not None and resistencia is not None:
        return (corriente**2) * resistencia
    elif voltaje is not None and resistencia is not None:
        if resistencia == 0:
            raise ValueError("La resistencia no puede ser cero para calcular la potencia.")
        return (voltaje**2) / resistencia
    else:
        raise ValueError("Se requieren al menos dos de los tres parámetros (voltaje, corriente, resistencia).")

def calcular_ley_kirchhoff_voltaje(voltajes: list[float]) -> float:
    """
    Calcula la suma de los voltajes en un lazo cerrado según la Ley de Voltajes de Kirchhoff.

    Args:
        voltajes (list): Una lista de voltajes en el lazo.

    Returns:
        float: La suma de los voltajes.
    """
    suma_voltajes = sum(voltajes)
    return suma_voltajes

def calcular_ley_kirchhoff_tension(corrientes: list[float]) -> float:
    """
    Calcula la suma de las corrientes que entran y salen de un nodo según la Ley de Corrientes de Kirchhoff.

    Args:
        corrientes (list): Una lista de corrientes (entrantes positivas, salientes negativas).

    Returns:
        float: La suma de las corrientes.
    """
    suma_corrientes = sum(corrientes)
    return suma_corrientes

def calcular_ley_kirchhoff_corriente(corrientes_entrantes: list[float]) -> float:
    """
    Calcula la corriente saliente total de un nodo utilizando la Ley de Corrientes de Kirchhoff (LCK).

    Args:
        corrientes_entrantes (list): Una lista de corrientes que entran al nodo en amperios (A).

    Returns:
        float: La corriente saliente.
    """
    corriente_saliente = sum(corrientes_entrantes)
    return corriente_saliente

def calcular_campo_magnetico(corriente, distancia, permeabilidad_vacio=4 * math.pi * (10**-7)) -> float:
    """
    Calcula el campo magnético (B) producido por un conductor largo y recto.

    Args:
        corriente (float): La corriente en amperios (A).
        distancia (float): La distancia perpendicular al conductor en metros (m).
        permeabilidad_vacio (float): La permeabilidad magnética del vacío (μ0).

    Returns:
        float: El campo magnético en teslas (T).

    Raises:
        ValueError: Si la distancia es cero.
    """
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    campo_magnetico = (permeabilidad_vacio * corriente) / (2 * math.pi * distancia)
    return campo_magnetico

def calcular_fuerza_lorentz(carga: float, velocidad: float, campo_magnetico: float, angulo_grados: float) -> float:
    """
    Calcula la fuerza de Lorentz sobre una partícula cargada en un campo magnético.

    Args:
        carga (float): La carga de la partícula en culombios (C).
        velocidad (float): La velocidad de la partícula en metros por segundo (m/s).
        campo_magnetico (float): La magnitud del campo magnético en teslas (T).
        angulo_grados (float): El ángulo entre la velocidad y el campo magnético en grados.

    Returns:
        float: La fuerza de Lorentz en newtons (N).
    """
    angulo_radianes = math.radians(angulo_grados)
    fuerza = carga * velocidad * campo_magnetico * math.sin(angulo_radianes)
    return fuerza

def calcular_potencial_electrico_carga_distancia(carga: float, distancia: float, k: float = 8.9875e9) -> float:
    """
    Calcula el potencial eléctrico (V) producido por una carga puntual a una distancia dada.

    Args:
        carga (float): La magnitud de la carga en culombios (C).
        distancia (float): La distancia desde la carga en metros (m).
        k (float): La constante de Coulomb (N·m²/C²).

    Returns:
        float: El potencial eléctrico en voltios (V).

    Raises:
        ValueError: Si la distancia es cero.
    """
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    potencial = (k * carga) / distancia
    return potencial

def calcular_potencial_electrico_energia_carga(energia_potencial: float, carga_prueba: float) -> float:
    """
    Calcula el potencial eléctrico (V) a partir de la energía potencial eléctrica y una carga de prueba.

    Args:
        energia_potencial (float): La energía potencial eléctrica en julios (J).
        carga_prueba (float): La carga de prueba en culombios (C).

    Returns:
        float: El potencial eléctrico en voltios (V).

    Raises:
        ValueError: Si la carga de prueba es cero.
    """
    if carga_prueba == 0:
        raise ValueError("La carga de prueba no puede ser cero.")
    potencial = energia_potencial / carga_prueba
    return potencial

def calcular_energia_potencial_electrica(carga: float, voltaje: float) -> float:
    """
    Calcula la energía potencial eléctrica (U) de una carga en un punto con un potencial eléctrico dado.

    Args:
        carga (float): La magnitud de la carga en culombios (C).
        voltaje (float): El potencial eléctrico en voltios (V).

    Returns:
        float: La energía potencial eléctrica en julios (J).
    """
    energia = carga * voltaje
    return energia

def calcular_potencial_electrico_distribucion_lineal(densidad_lineal_carga: float, longitud: float, distancia: float, k: float = 8.9875e9) -> float:
    """
    Calcula el potencial eléctrico de una distribución de carga lineal uniforme en un punto a una distancia perpendicular del centro.
    Esta es una aproximación simplificada y puede no ser precisa para todos los casos.

    Args:
        densidad_lineal_carga (float): Densidad de carga lineal (C/m).
        longitud (float): Longitud de la distribución lineal (m).
        distancia (float): Distancia perpendicular desde el centro de la línea al punto (m).
        k (float): Constante de Coulomb (N·m²/C²).

    Returns:
        float: Potencial eléctrico en voltios (V).
    """
    # Aproximación para un hilo infinito o muy largo, o para puntos muy alejados
    # Para un cálculo más preciso se necesitaría integración.
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    # Simplificación: tratar como una carga puntual equivalente en el centro para distancias grandes
    carga_total = densidad_lineal_carga * longitud
    return (k * carga_total) / distancia

def calcular_potencial_electrico_distribucion_superficial(densidad_superficial_carga: float, area: float, distancia: float, k: float = 8.9875e9) -> float:
    """
    Calcula el potencial eléctrico de una distribución de carga superficial uniforme en un punto.
    Esta es una aproximación simplificada y puede no ser precisa para todos los casos.

    Args:
        densidad_superficial_carga (float): Densidad de carga superficial (C/m^2).
        area (float): Área de la distribución superficial (m^2).
        distancia (float): Distancia desde la distribución al punto (m).
        k (float): Constante de Coulomb (N·m²/C²).

    Returns:
        float: Potencial eléctrico en voltios (V).
    """
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    # Simplificación: tratar como una carga puntual equivalente en el centro para distancias grandes
    carga_total = densidad_superficial_carga * area
    return (k * carga_total) / distancia

def calcular_potencial_electrico_distribucion_volumetrica(densidad_volumetrica_carga: float, volumen: float, distancia: float, k: float = 8.9875e9) -> float:
    """
    Calcula el potencial eléctrico de una distribución de carga volumétrica uniforme en un punto.
    Esta es una aproximación simplificada y puede no ser precisa para todos los casos.

    Args:
        densidad_volumetrica_carga (float): Densidad de carga volumétrica (C/m^3).
        volumen (float): Volumen de la distribución volumétrica (m^3).
        distancia (float): Distancia desde la distribución al punto (m).
        k (float): Constante de Coulomb (N·m²/C²).

    Returns:
        float: Potencial eléctrico en voltios (V).
    """
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    # Simplificación: tratar como una carga puntual equivalente en el centro para distancias grandes
    carga_total = densidad_volumetrica_carga * volumen
    return (k * carga_total) / distancia

def calcular_flujo_magnetico(campo_magnetico: float, area: float, angulo_grados: float) -> float:
    """
    Calcula el flujo magnético (Φ) a través de una superficie.

    Args:
        campo_magnetico (float): La magnitud del campo magnético en teslas (T).
        area (float): El área de la superficie en metros cuadrados (m²).
        angulo_grados (float): El ángulo entre el vector normal al área y el campo magnético en grados.

    Returns:
        float: El flujo magnético en webers (Wb).
    """
    angulo_radianes = math.radians(angulo_grados)
    flujo_magnetico = campo_magnetico * area * math.cos(angulo_radianes)
    return flujo_magnetico

def calcular_ley_faraday(cambio_flujo_magnetico: float, cambio_tiempo: float, numero_espiras: int = 1) -> float:
    """
    Calcula la fuerza electromotriz (FEM) inducida según la Ley de Faraday.

    Args:
        cambio_flujo_magnetico (float): El cambio en el flujo magnético en webers (Wb).
        cambio_tiempo (float): El cambio en el tiempo en segundos (s).
        numero_espiras (int): El número de espiras en la bobina.

    Returns:
        float: La fuerza electromotriz (FEM) en voltios (V).

    Raises:
        ValueError: Si el cambio de tiempo es cero.
    """
    if cambio_tiempo == 0:
        raise ValueError("El cambio en el tiempo no puede ser cero.")
    fem = -numero_espiras * (cambio_flujo_magnetico / cambio_tiempo)
    return fem

def calcular_potencia_electrica(voltaje: float, corriente: float) -> float:
    """
    Calcula la potencia eléctrica (P) dado el voltaje (V) y la corriente (I).

    Args:
        voltaje (float): El voltaje en voltios (V).
        corriente (float): La corriente en amperios (A).

    Returns:
        float: La potencia eléctrica en vatios (W).
    """
    potencia = voltaje * corriente
    return potencia

def calcular_energia_electrica(potencia: float, tiempo: float) -> float:
    """
    Calcula la energía eléctrica consumida.

    Args:
        potencia (float): La potencia en vatios (W).
        tiempo (float): El tiempo en horas (h).

    Returns:
        float: La energía eléctrica en kilovatios-hora (kWh).
    """
    energia = (potencia * tiempo) / 1000
    return energia

def calcular_voltaje_caida(corriente: float, resistencia: float) -> float:
    """
    Calcula la caída de voltaje en un circuito.

    Args:
        corriente (float): La corriente en amperios (A).
        resistencia (float): La resistencia en ohmios (Ω).

    Returns:
        float: La caída de voltaje en voltios (V).
    """
    voltaje_caida = corriente * resistencia
    return voltaje_caida

def calcular_eficiencia_electrica(potencia_salida: float, potencia_entrada: float) -> float:
    """
    Calcula la eficiencia eléctrica (η) dado la potencia de salida y la potencia de entrada.

    Args:
        potencia_salida (float): La potencia de salida en vatios (W).
        potencia_entrada (float): La potencia de entrada en vatios (W).

    Returns:
        float: La eficiencia eléctrica (sin unidades).
    """
    if potencia_entrada == 0:
        raise ValueError("La potencia de entrada no puede ser cero.")
    eficiencia = potencia_salida / potencia_entrada
    return eficiencia

def calcular_potencial_electrico_carga_puntual(carga: float, distancia: float, k: float = 8.9875e9) -> float:
    """
    Calcula el potencial eléctrico (V) producido por una carga puntual.

    Args:
        carga (float): La magnitud de la carga en culombios (C).
        distancia (float): La distancia desde la carga en metros (m).
        k (float): La constante de Coulomb (N·m²/C²).

    Returns:
        float: El potencial eléctrico en voltios (V).

    Raises:
        ValueError: Si la distancia es cero.
    """
    if distancia == 0:
        raise ValueError("La distancia no puede ser cero.")
    potencial_electrico = (k * carga) / distancia
    return potencial_electrico

def calcular_energia_potencial_electrica(carga_prueba: float, potencial_electrico: float) -> float:
    """
    Calcula la energía potencial eléctrica (U) de una carga de prueba en un potencial eléctrico.

    Args:
        carga_prueba (float): La magnitud de la carga de prueba en culombios (C).
        potencial_electrico (float): La magnitud del potencial eléctrico en voltios (V).

    Returns:
        float: La energía potencial eléctrica en julios (J).
    """
    energia_potencial_electrica = carga_prueba * potencial_electrico
    return energia_potencial_electrica

def calcular_resistencia(voltaje: float, corriente: float) -> float:
    """
    Calcula la resistencia utilizando la Ley de Ohm.

    Args:
        voltaje (float): El voltaje en voltios (V).
        corriente (float): La corriente en amperios (A).

    Returns:
        float: La resistencia en ohmios (Ω).
    """
    if corriente == 0:
        raise ValueError("La corriente no puede ser cero para calcular la resistencia.")
    resistencia = voltaje / corriente
    return resistencia