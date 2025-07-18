from flask_restx import fields, Api

def init_schemas(api: Api):
    # Modelos de datos para Cinemática
    caida_libre_model = api.model('CaidaLibreInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de caída libre (tiempo_caida, velocidad_final, altura_en_tiempo)'),
        'altura_inicial': fields.Float(required=False, description='Altura inicial desde la que cae el objeto (m)'),
        'tiempo': fields.Float(required=False, description='Tiempo transcurrido (s)')
    })

    tiro_parabolico_model = api.model('TiroParabolicoInput', {
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'angulo_grados': fields.Float(required=True, description='Ángulo de lanzamiento en grados'),
        'altura_inicial': fields.Float(required=False, default=0.0, description='Altura inicial (m)'),

    })

    movimiento_circular_uniforme_model = api.model('MovimientoCircularUniformeInput', {
        'radio': fields.Float(required=True, description='Radio de la trayectoria circular (m)'),
        'velocidad_angular': fields.Float(required=True, description='Velocidad angular (rad/s)'),

    })

    pendulo_simple_model = api.model('PenduloSimpleInput', {
        'longitud': fields.Float(required=True, description='Longitud del péndulo (m)'),
        'angulo_inicial_grados': fields.Float(required=True, description='Ángulo inicial en grados'),
        'velocidad_angular_inicial': fields.Float(required=False, default=0.0, description='Velocidad angular inicial (rad/s)'),

    })

    movimiento_armonico_simple_model = api.model('MovimientoArmonicoSimpleInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo (periodo_frecuencia, posicion, velocidad, aceleracion)'),
        'amplitud': fields.Float(required=True, description='Amplitud (m)'),
        'frecuencia_angular': fields.Float(required=True, description='Frecuencia angular (rad/s)'),
        'fase_inicial': fields.Float(required=False, default=0.0, description='Fase inicial (rad)'),
        'tiempo': fields.Float(required=False, description='Tiempo (s)')
    })

    mru_model = api.model('MRUInput', {
        'posicion_inicial': fields.Float(required=True, description='Posición inicial (m)'),
        'velocidad': fields.Float(required=True, description='Velocidad constante (m/s)'),

    })

    mruv_model = api.model('MRUVInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo (posicion, velocidad)'),
        'posicion_inicial': fields.Float(required=False, default=0.0, description='Posición inicial (m)'),
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'aceleracion': fields.Float(required=True, description='Aceleración constante (m/s^2)'),
        'tiempo': fields.Float(required=True, description='Tiempo transcurrido (s)')
    })

    # Modelos de datos para Colisiones
    colision_elastica_1d_model = api.model('ColisionElastica1DInput', {
        'masa1': fields.Float(required=True, description='Masa del objeto 1 (kg)'),
        'velocidad_inicial1': fields.Float(required=True, description='Velocidad inicial del objeto 1 (m/s)'),
        'masa2': fields.Float(required=True, description='Masa del objeto 2 (kg)'),
        'velocidad_inicial2': fields.Float(required=True, description='Velocidad inicial del objeto 2 (m/s)')
    })

    colision_elastica_2d_model = api.model('ColisionElastica2DInput', {
        'masa1': fields.Float(required=True, description='Masa del objeto 1 (kg)'),
        'velocidad_inicial1': fields.Float(required=True, description='Velocidad inicial del objeto 1 (m/s)'),
        'angulo_inicial1_grados': fields.Float(required=True, description='Ángulo inicial del objeto 1 en grados'),
        'masa2': fields.Float(required=True, description='Masa del objeto 2 (kg)'),
        'velocidad_inicial2': fields.Float(required=True, description='Velocidad inicial del objeto 2 (m/s)'),
        'angulo_inicial2_grados': fields.Float(required=True, description='Ángulo inicial del objeto 2 en grados')
    })

    colision_elastica_3d_model = api.model('ColisionElastica3DInput', {
        'masa1': fields.Float(required=True, description='Masa del objeto 1 (kg)'),
        'velocidad_inicial1_x': fields.Float(required=True, description='Componente X de la velocidad inicial del objeto 1 (m/s)'),
        'velocidad_inicial1_y': fields.Float(required=True, description='Componente Y de la velocidad inicial del objeto 1 (m/s)'),
        'velocidad_inicial1_z': fields.Float(required=True, description='Componente Z de la velocidad inicial del objeto 1 (m/s)'),
        'masa2': fields.Float(required=True, description='Masa del objeto 2 (kg)'),
        'velocidad_inicial2_x': fields.Float(required=True, description='Componente X de la velocidad inicial del objeto 2 (m/s)'),
        'velocidad_inicial2_y': fields.Float(required=True, description='Componente Y de la velocidad inicial del objeto 2 (m/s)'),
        'velocidad_inicial2_z': fields.Float(required=True, description='Componente Z de la velocidad inicial del objeto 2 (m/s)'),
        'normal_x': fields.Float(required=True, description='Componente X del vector normal a la superficie de colisión'),
        'normal_y': fields.Float(required=True, description='Componente Y del vector normal a la superficie de colisión'),
        'normal_z': fields.Float(required=True, description='Componente Z del vector normal a la superficie de colisión')
    })

    colision_perfectamente_inelastica_1d_model = api.model('ColisionPerfectamenteInelastica1DInput', {
        'masa1': fields.Float(required=True, description='Masa del objeto 1 (kg)'),
        'velocidad_inicial1': fields.Float(required=True, description='Velocidad inicial del objeto 1 (m/s)'),
        'masa2': fields.Float(required=True, description='Masa del objeto 2 (kg)'),
        'velocidad_inicial2': fields.Float(required=True, description='Velocidad inicial del objeto 2 (m/s)')
    })

    colision_perfectamente_inelastica_2d_model = api.model('ColisionPerfectamenteInelastica2DInput', {
        'masa1': fields.Float(required=True, description='Masa del objeto 1 (kg)'),
        'velocidad_inicial1_x': fields.Float(required=True, description='Componente X de la velocidad inicial del objeto 1 (m/s)'),
        'velocidad_inicial1_y': fields.Float(required=True, description='Componente Y de la velocidad inicial del objeto 1 (m/s)'),
        'masa2': fields.Float(required=True, description='Masa del objeto 2 (kg)'),
        'velocidad_inicial2_x': fields.Float(required=True, description='Componente X de la velocidad inicial del objeto 2 (m/s)'),
        'velocidad_inicial2_y': fields.Float(required=True, description='Componente Y de la velocidad inicial del objeto 2 (m/s)')
    })

    # Modelos de datos para Dinámica
    leyes_newton_model = api.model('LeyesNewtonInput', {
        'masa': fields.Float(required=True, description='Masa del objeto (kg)'),
        'fuerza_aplicada': fields.Float(required=True, description='Fuerza aplicada (N)'),
        'coeficiente_rozamiento_estatico': fields.Float(required=False, default=0.0, description='Coeficiente de rozamiento estático'),
        'coeficiente_rozamiento_cinetico': fields.Float(required=False, default=0.0, description='Coeficiente de rozamiento cinético')
    })

    plano_inclinado_model = api.model('PlanoInclinadoInput', {
        'masa': fields.Float(required=True, description='Masa del objeto (kg)'),
        'angulo_inclinacion_grados': fields.Float(required=True, description='Ángulo de inclinación del plano en grados'),
        'coeficiente_rozamiento_estatico': fields.Float(required=True, description='Coeficiente de rozamiento estático'),
        'coeficiente_rozamiento_cinetico': fields.Float(required=True, description='Coeficiente de rozamiento cinético'),
        'distancia_plano': fields.Float(required=True, description='Distancia del plano (m)'),
        'velocidad_inicial': fields.Float(required=False, default=0.0, description='Velocidad inicial (m/s)')
    })

    plano_inclinado_polea_model = api.model('PlanoInclinadoPoleaInput', {
        'masa1': fields.Float(required=True, description='Masa del objeto en el plano (kg)'),
        'masa2': fields.Float(required=True, description='Masa del objeto colgante (kg)'),
        'angulo_inclinacion_grados': fields.Float(required=True, description='Ángulo de inclinación del plano en grados'),
        'coeficiente_rozamiento_estatico': fields.Float(required=True, description='Coeficiente de rozamiento estático'),
        'coeficiente_rozamiento_cinetico': fields.Float(required=True, description='Coeficiente de rozamiento cinético')
    })

    # Modelos de datos para Energía
    trabajo_energia_cinetica_model = api.model('TrabajoEnergiaCineticaInput', {
        'masa': fields.Float(required=True, description='Masa del objeto (kg)'),
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'velocidad_final': fields.Float(required=True, description='Velocidad final (m/s)')
    })

    energia_potencial_gravitatoria_model = api.model('EnergiaPotencialGravitatoriaInput', {
        'masa': fields.Float(required=True, description='Masa del objeto (kg)'),
        'altura': fields.Float(required=True, description='Altura (m)')
    })

    energia_potencial_elastica_model = api.model('EnergiaPotencialElasticaInput', {
        'constante_elastica': fields.Float(required=True, description='Constante elástica del resorte (N/m)'),
        'deformacion': fields.Float(required=True, description='Deformación del resorte (m)')
    })

    # Modelos de datos para Electricidad y Magnetismo
    ley_kirchhoff_voltaje_model = api.model('LeyKirchhoffVoltajeInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de Ley de Kirchhoff de Voltaje (voltajes)'),
        'voltajes': fields.List(fields.Float, required=False, description='Lista de voltajes en el lazo (V)')
    })

    ley_kirchhoff_corriente_model = api.model('LeyKirchhoffCorrienteInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de Ley de Kirchhoff de Corriente (corrientes)'),
        'corrientes_entrantes': fields.List(fields.Float, required=False, description='Lista de corrientes que entran al nodo (A)'),
        'corrientes_salientes': fields.List(fields.Float, required=False, description='Lista de corrientes que salen del nodo (A)')
    })

    capacitancia_model = api.model('CapacitanciaInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de capacitancia (capacitancia, carga, voltaje, energia)'),
        'carga': fields.Float(required=False, description='Carga en el capacitor (C)'),
        'voltaje': fields.Float(required=False, description='Voltaje a través del capacitor (V)'),
        'capacitancia': fields.Float(required=False, description='Capacitancia (F)')
    })

    circuito_serie_model = api.model('CircuitoSerieInput', {
        'resistencias': fields.List(fields.Float, required=True, description='Lista de resistencias en serie (Ohms)'),
        'voltaje_total': fields.Float(required=False, description='Voltaje total de la fuente (V)')
    })

    circuito_paralelo_model = api.model('CircuitoParaleloInput', {
        'resistencias': fields.List(fields.Float, required=True, description='Lista de resistencias en paralelo (Ohms)'),
        'voltaje_total': fields.Float(required=False, description='Voltaje total de la fuente (V)')
    })

    potencia_electrica_model = api.model('PotenciaElectricaInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de potencia (ley_ohm, resistencia, voltaje)'),
        'voltaje': fields.Float(required=False, description='Voltaje (V)'),
        'corriente': fields.Float(required=False, description='Corriente (A)'),
        'resistencia': fields.Float(required=False, description='Resistencia (Ohms)')
    })

    ley_ohm_model = api.model('LeyOhmInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo (voltaje, corriente, resistencia)'),
        'voltaje': fields.Float(required=False, description='Voltaje (V)'),
        'corriente': fields.Float(required=False, description='Corriente (A)'),
        'resistencia': fields.Float(required=False, description='Resistencia (Ohms)')
    })

    inductancia_model = api.model('InductanciaInput', {
        'flujo_magnetico': fields.Float(required=True, description='Flujo magnético (Weber)'),
        'corriente': fields.Float(required=True, description='Corriente (A)'),
        'numero_espiras': fields.Integer(required=True, description='Número de espiras')
    })

    energia_inductor_model = api.model('EnergiaInductorInput', {
        'inductancia': fields.Float(required=True, description='Inductancia (H)'),
        'corriente': fields.Float(required=True, description='Corriente (A)')
    })

    campo_magnetico_model = api.model('CampoMagneticoInput', {
        'corriente': fields.Float(required=True, description='Corriente (A)'),
        'distancia': fields.Float(required=True, description='Distancia al conductor (m)')
    })

    flujo_magnetico_model = api.model('FlujoMagneticoInput', {
        'campo_magnetico': fields.Float(required=True, description='Campo magnético (T)'),
        'area': fields.Float(required=True, description='Área (m^2)'),
        'angulo_grados': fields.Float(required=True, description='Ángulo entre el campo y la normal al área en grados')
    })

    fuerza_magnetica_model = api.model('FuerzaMagneticaInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de fuerza magnética (conductor, carga_movil)'),
        'corriente': fields.Float(required=False, description='Corriente en el conductor (A)'),
        'longitud': fields.Float(required=False, description='Longitud del conductor (m)'),
        'campo_magnetico': fields.Float(required=False, description='Campo magnético (T)'),
        'angulo_grados': fields.Float(required=False, description='Ángulo entre la corriente y el campo magnético en grados'),
        'carga': fields.Float(required=False, description='Carga de la partícula (C)'),
        'velocidad': fields.Float(required=False, description='Velocidad de la partícula (m/s)')
    })

    fuerza_lorentz_model = api.model('FuerzaLorentzInput', {
        'carga': fields.Float(required=True, description='Carga de la partícula (C)'),
        'velocidad': fields.Float(required=True, description='Velocidad de la partícula (m/s)'),
        'campo_magnetico': fields.Float(required=True, description='Campo magnético (T)'),
        'angulo_grados': fields.Float(required=True, description='Ángulo entre la velocidad y el campo magnético en grados')
    })

    ley_faraday_model = api.model('LeyFaradayInput', {
        'cambio_flujo_magnetico': fields.Float(required=False, description='Cambio en el flujo magnético (Weber)'),
        'cambio_tiempo': fields.Float(required=False, description='Cambio en el tiempo (s)'),
        'num_espiras': fields.Integer(required=False, description='Número de espiras')
    })

    magnetismo_model = api.model('MagnetismoInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de magnetismo (campo_magnetico, flujo_magnetico, fuerza_lorentz, ley_faraday)'),
        'corriente': fields.Float(required=False, description='Corriente (A) para campo magnético'),
        'distancia': fields.Float(required=False, description='Distancia (m) para campo magnético'),
        'campo_magnetico': fields.Float(required=False, description='Campo magnético (T) para flujo magnético y fuerza de Lorentz'),
        'area': fields.Float(required=False, description='Área (m^2) para flujo magnético'),
        'angulo': fields.Float(required=False, description='Ángulo (grados) para flujo magnético y fuerza de Lorentz'),
        'carga': fields.Float(required=False, description='Carga (C) para fuerza de Lorentz'),
        'velocidad': fields.Float(required=False, description='Velocidad (m/s) para fuerza de Lorentz'),
        'num_espiras': fields.Integer(required=False, description='Número de espiras para ley de Faraday'),
        'cambio_flujo': fields.Float(required=False, description='Cambio de flujo (Weber) para ley de Faraday'),
        'cambio_tiempo': fields.Float(required=False, description='Cambio de tiempo (s) para ley de Faraday')
    })

    ley_ohm_model = api.model('LeyOhmInput', {
        'voltaje': fields.Float(required=False, description='Voltaje (V)'),
        'corriente': fields.Float(required=False, description='Corriente (A)'),
        'resistencia': fields.Float(required=False, description='Resistencia (Ohms)')
    })

    ondas_mecanicas_model = api.model('OndasMecanicasInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de ondas mecánicas (velocidad_onda, frecuencia_onda, longitud_onda, periodo_onda, velocidad_cuerda)'),
        'velocidad': fields.Float(required=False, description='Velocidad de la onda (m/s)'),
        'frecuencia': fields.Float(required=False, description='Frecuencia de la onda (Hz)'),
        'longitud_onda': fields.Float(required=False, description='Longitud de onda (m)'),
        'periodo': fields.Float(required=False, description='Período de la onda (s)'),
        'tension': fields.Float(required=False, description='Tensión en la cuerda (N)'),
        'densidad_lineal': fields.Float(required=False, description='Densidad lineal de la cuerda (kg/m)')
    })

    resistencia_model = api.model('ResistenciaInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de resistencia (ley_ohm, material)'),
        'voltaje': fields.Float(required=False, description='Voltaje (V)'),
        'corriente': fields.Float(required=False, description='Corriente (A)'),
        'resistividad': fields.Float(required=False, description='Resistividad del material (Ohm*m)'),
        'longitud': fields.Float(required=False, description='Longitud del conductor (m)'),
        'area': fields.Float(required=False, description='Área de la sección transversal del conductor (m^2)')
    })

    ley_gauss_model = api.model('LeyGaussInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de Ley de Gauss (flujo_electrico_carga, flujo_electrico_campo_area)'),
        'carga_encerrada': fields.Float(required=False, description='Carga encerrada (C)'),
        'campo_electrico': fields.Float(required=False, description='Campo eléctrico (N/C)'),
        'area': fields.Float(required=False, description='Área (m^2)'),
        'angulo': fields.Float(required=False, description='Ángulo entre el campo eléctrico y la normal a la superficie en grados')
    })

    potencial_electrico_model = api.model('PotencialElectricoInput', {
        'tipo_calculo': fields.String(required=True, description='Tipo de cálculo de potencial eléctrico (punto, distribucion_lineal, distribucion_superficial, distribucion_volumetrica)'),
        'carga': fields.Float(required=False, description='Carga puntual (C)'),
        'distancia': fields.Float(required=False, description='Distancia desde la carga (m)'),
        'densidad_lineal_carga': fields.Float(required=False, description='Densidad de carga lineal (C/m)'),
        'longitud': fields.Float(required=False, description='Longitud de la distribución lineal (m)'),
        'densidad_superficial_carga': fields.Float(required=False, description='Densidad de carga superficial (C/m^2)'),
        'area': fields.Float(required=False, description='Área de la distribución superficial (m^2)'),
        'densidad_volumetrica_carga': fields.Float(required=False, description='Densidad de carga volumétrica (C/m^3)'),
        'volumen': fields.Float(required=False, description='Volumen de la distribución volumétrica (m^3)')
    })

    # Modelos de datos para Ondas
    longitud_onda_model = api.model('LongitudOndaInput', {
        'velocidad': fields.Float(required=True, description='Velocidad de la onda (m/s)'),
        'frecuencia': fields.Float(required=True, description='Frecuencia de la onda (Hz)')
    })

    frecuencia_onda_model = api.model('FrecuenciaOndaInput', {
        'velocidad': fields.Float(required=True, description='Velocidad de la onda (m/s)'),
        'longitud_onda': fields.Float(required=True, description='Longitud de la onda (m)')
    })

    velocidad_onda_model = api.model('VelocidadOndaInput', {
        'longitud_onda': fields.Float(required=True, description='Longitud de la onda (m)'),
        'frecuencia': fields.Float(required=True, description='Frecuencia de la onda (Hz)')
    })

    # Modelos de datos para Ecuaciones Cinemáticas
    velocidad_final_tiempo_model = api.model('VelocidadFinalTiempoInput', {
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'aceleracion': fields.Float(required=True, description='Aceleración (m/s^2)'),
        'tiempo': fields.Float(required=True, description='Tiempo (s)')
    })

    posicion_final_tiempo_model = api.model('PosicionFinalTiempoInput', {
        'posicion_inicial': fields.Float(required=True, description='Posición inicial (m)'),
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'aceleracion': fields.Float(required=True, description='Aceleración (m/s^2)'),
        'tiempo': fields.Float(required=True, description='Tiempo (s)')
    })

    velocidad_final_desplazamiento_model = api.model('VelocidadFinalDesplazamientoInput', {
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'aceleracion': fields.Float(required=True, description='Aceleración (m/s^2)'),
        'desplazamiento': fields.Float(required=True, description='Desplazamiento (m)')
    })

    desplazamiento_velocidades_model = api.model('DesplazamientoVelocidadesInput', {
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'velocidad_final': fields.Float(required=True, description='Velocidad final (m/s)'),
        'tiempo': fields.Float(required=True, description='Tiempo (s)')
    })

    tiempo_desplazamiento_velocidades_model = api.model('TiempoDesplazamientoVelocidadesInput', {
        'desplazamiento': fields.Float(required=True, description='Desplazamiento (m)'),
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'velocidad_final': fields.Float(required=True, description='Velocidad final (m/s)')
    })

    aceleracion_velocidades_tiempo_model = api.model('AceleracionVelocidadesTiempoInput', {
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'velocidad_final': fields.Float(required=True, description='Velocidad final (m/s)'),
        'tiempo': fields.Float(required=True, description='Tiempo (s)')
    })

    tiempo_posicion_velocidad_aceleracion_model = api.model('TiempoPosicionVelocidadAceleracionInput', {
        'posicion_inicial': fields.Float(required=True, description='Posición inicial (m)'),
        'posicion_final': fields.Float(required=True, description='Posición final (m)'),
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'aceleracion': fields.Float(required=True, description='Aceleración (m/s^2)')
    })

    aceleracion_posicion_velocidad_tiempo_model = api.model('AceleracionPosicionVelocidadTiempoInput', {
        'posicion_inicial': fields.Float(required=True, description='Posición inicial (m)'),
        'posicion_final': fields.Float(required=True, description='Posición final (m)'),
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'tiempo': fields.Float(required=True, description='Tiempo (s)')
    })

    posicion_final_velocidad_aceleracion_model = api.model('PosicionFinalVelocidadAceleracionInput', {
        'posicion_inicial': fields.Float(required=True, description='Posición inicial (m)'),
        'velocidad_inicial': fields.Float(required=True, description='Velocidad inicial (m/s)'),
        'velocidad_final': fields.Float(required=True, description='Velocidad final (m/s)'),
        'aceleracion': fields.Float(required=True, description='Aceleración (m/s^2)')
    })

    return {
        'caida_libre_model': caida_libre_model,
        'tiro_parabolico_model': tiro_parabolico_model,
        'movimiento_circular_uniforme_model': movimiento_circular_uniforme_model,
        'pendulo_simple_model': pendulo_simple_model,
        'movimiento_armonico_simple_model': movimiento_armonico_simple_model,
        'mru_model': mru_model,
        'mruv_model': mruv_model,
        'colision_elastica_1d_model': colision_elastica_1d_model,
        'colision_elastica_2d_model': colision_elastica_2d_model,
        'colision_elastica_3d_model': colision_elastica_3d_model,
        'colision_perfectamente_inelastica_1d_model': colision_perfectamente_inelastica_1d_model,
        'colision_perfectamente_inelastica_2d_model': colision_perfectamente_inelastica_2d_model,
        'leyes_newton_model': leyes_newton_model,
        'plano_inclinado_model': plano_inclinado_model,
        'plano_inclinado_polea_model': plano_inclinado_polea_model,
        'trabajo_energia_cinetica_model': trabajo_energia_cinetica_model,
        'energia_potencial_gravitatoria_model': energia_potencial_gravitatoria_model,
        'energia_potencial_elastica_model': energia_potencial_elastica_model,
        'ley_kirchhoff_voltaje_model': ley_kirchhoff_voltaje_model,
        'ley_kirchhoff_corriente_model': ley_kirchhoff_corriente_model,
        'capacitancia_model': capacitancia_model,
        'circuito_serie_model': circuito_serie_model,
        'circuito_paralelo_model': circuito_paralelo_model,
        'potencia_electrica_model': potencia_electrica_model,
        'inductancia_model': inductancia_model,
        'campo_magnetico_model': campo_magnetico_model,
        'flujo_magnetico_model': flujo_magnetico_model,
        'fuerza_magnetica_model': fuerza_magnetica_model,
        'fuerza_lorentz_model': fuerza_lorentz_model,
        'ley_faraday_model': ley_faraday_model,
        'magnetismo_model': magnetismo_model,
        'ley_ohm_model': ley_ohm_model,
        'ondas_mecanicas_model': ondas_mecanicas_model,
        'resistencia_model': resistencia_model,
        'ley_gauss_model': ley_gauss_model,
        'potencial_electrico_model': potencial_electrico_model,
        'longitud_onda_model': longitud_onda_model,
        'frecuencia_onda_model': frecuencia_onda_model,
        'velocidad_onda_model': velocidad_onda_model,
        'velocidad_final_tiempo_model': velocidad_final_tiempo_model,
        'posicion_final_tiempo_model': posicion_final_tiempo_model,
        'velocidad_final_desplazamiento_model': velocidad_final_desplazamiento_model,
        'desplazamiento_velocidades_model': desplazamiento_velocidades_model,
        'tiempo_desplazamiento_velocidades_model': tiempo_desplazamiento_velocidades_model,
        'aceleracion_velocidades_tiempo_model': aceleracion_velocidades_tiempo_model,
        'tiempo_posicion_velocidad_aceleracion_model': tiempo_posicion_velocidad_aceleracion_model,
        'aceleracion_posicion_velocidad_tiempo_model': aceleracion_posicion_velocidad_tiempo_model,
        'posicion_final_velocidad_aceleracion_model': posicion_final_velocidad_aceleracion_model,
    }