from flask import Flask, jsonify
from flask_restx import Api, Resource
from flask_restx import Api as ApiX, Namespace, fields
from schemas import init_schemas

# Importaciones de cinemática
from .simulations.cinematica.caida_libre import simular_caida_libre
from .simulations.cinematica.tiro_parabolico import simular_tiro_parabolico
from .simulations.cinematica.movimiento_circular_uniforme import simular_movimiento_circular_uniforme
from .simulations.cinematica.pendulo import simular_pendulo_simple
from .simulations.cinematica.movimiento_armonico_simple import simular_movimiento_armonico_simple
from .simulations.cinematica.mru import simular_mru
from .simulations.cinematica.mruv import simular_mruv

# Importaciones de colisiones
from .simulations.colisiones.colision_elastica_1d import simular_colision_elastica_1d
from .simulations.colisiones.colision_elastica_2d import simular_colision_elastica_2d
from .simulations.colisiones.colision_elastica_3d import simular_colision_elastica_3d
from .simulations.colisiones.colision_perfectamente_inelastica_1d import simular_colision_perfectamente_inelastica_1d
from .simulations.colisiones.colision_perfectamente_inelastica_2d import simular_colision_perfectamente_inelastica_2d

# Importaciones de dinámica
from .simulations.dinamica.leyes_newton import simular_leyes_newton
from .simulations.dinamica.plano_inclinado import simular_plano_inclinado
from .simulations.dinamica.plano_inclinado_polea import simular_plano_inclinado_polea

# Importaciones de energía
from .simulations.energia.trabajo_energia import simular_trabajo_energia_cinetica
from .simulations.energia.energia_potencial_gravitatoria import simular_energia_potencial_gravitatoria
from .simulations.energia.energia_potencial_elastica import simular_energia_potencial_elastica

# Importaciones de electricidad y magnetismo
from .simulations.electricidad_y_magnetismo.leyes_kirchhoff import simular_ley_kirchhoff_voltaje, simular_ley_kirchhoff_corriente
from .simulations.electricidad_y_magnetismo.capacitancia import simular_capacitancia
from .simulations.electricidad_y_magnetismo.calculos_circuitos import simular_circuito_serie, simular_circuito_paralelo
from .simulations.electricidad_y_magnetismo.potencia_electrica import simular_potencia_electrica
from .simulations.electricidad_y_magnetismo.inductancia import simular_inductancia
from .simulations.electricidad_y_magnetismo.magnetismo import simular_campo_magnetico, simular_flujo_magnetico, simular_fuerza_lorentz, simular_ley_faraday
from .simulations.electricidad_y_magnetismo.ley_ohm import simular_ley_ohm
from .simulations.electricidad_y_magnetismo.resistencia import simular_resistencia

# Importaciones de ondas
from .simulations.ondas.ondas import simular_longitud_onda, simular_frecuencia_onda, simular_velocidad_onda

# Importaciones de ecuaciones cinemáticas
from .Ecuaciones.cinematica.ecuaciones_cinematicas import (
    calcular_desplazamiento_velocidades,
    calcular_velocidad_final_desplazamiento,
    calcular_tiempo_desplazamiento_velocidades,
    calcular_velocidad_final_tiempo,
    calcular_posicion_final_tiempo,
    calcular_aceleracion_velocidades_tiempo,
    calcular_tiempo_posicion_velocidad_aceleracion,
    calcular_posicion_final_velocidad_aceleracion
)
from .Ecuaciones.colisiones.colision_elastica_1d import calcular_colision_elastica_1d
from .Ecuaciones.colisiones.colision_elastica_2d import calcular_colision_elastica_2d
from .Ecuaciones.colisiones.colision_elastica_3d import calcular_colision_elastica_3d
from .Ecuaciones.colisiones.colision_perfectamente_inelastica_1d import calcular_colision_perfectamente_inelastica_1d
from .Ecuaciones.colisiones.colision_perfectamente_inelastica_2d import calcular_colision_perfectamente_inelastica_2d
from .Ecuaciones.energia.energia_potencial_elastica import calcular_energia_potencial_elastica
from .Ecuaciones.energia.energia_potencial_gravitatoria import calcular_energia_potencial_gravitatoria
from .Ecuaciones.energia.trabajo_energia import calcular_trabajo_energia_cinetica
from .Ecuaciones.ondas.ondas import calcular_longitud_onda, calcular_frecuencia_onda, calcular_velocidad_onda

app = Flask(__name__)
api = ApiX(app, version='1.0', title='API de Simulador de Física', description='API para cálculos y simulaciones de física')

# Inicializar esquemas de modelos
models = init_schemas(api)

# Namespaces para organizar la API
ns_cinematica = api.namespace('cinematica', description='Operaciones relacionadas con Cinemática')
ns_colisiones = api.namespace('colisiones', description='Operaciones relacionadas con Colisiones')
ns_dinamica = api.namespace('dinamica', description='Operaciones relacionadas con Dinámica')
ns_energia = api.namespace('energia', description='Operaciones relacionadas con Energía')
ns_electricidad_magnetismo = api.namespace('electricidad-magnetismo', description='Operaciones relacionadas con Electricidad y Magnetismo')
ns_ondas = api.namespace('ondas', description='Operaciones relacionadas con Ondas')



@ns_cinematica.route('/caida-libre')
class CaidaLibre(Resource):
    @ns_cinematica.expect(models['caida_libre_model'])
    @ns_cinematica.response(200, 'Success', api.model('CaidaLibreOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_cinematica.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        altura_inicial = data.get('altura_inicial')
        tiempo = data.get('tiempo')

        try:
            if tipo_calculo == 'tiempo_caida':
                if altura_inicial is None or altura_inicial <= 0:
                    raise ValueError("Para 'tiempo_caida', 'altura_inicial' debe ser un valor positivo.")
                tiempo_caida = calcular_tiempo_caida(altura_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de tiempo de caída libre exitoso.",
                    "parametros_entrada": {"altura_inicial": altura_inicial},
                    "resultados": {"tiempo_caida": f"{tiempo_caida:.4f} s"}
                })
            elif tipo_calculo == 'velocidad_final':
                if altura_inicial is None or altura_inicial <= 0:
                    raise ValueError("Para 'velocidad_final', 'altura_inicial' debe ser un valor positivo.")
                velocidad_final = calcular_velocidad_final_caida_libre(altura_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de velocidad final en caída libre exitoso.",
                    "parametros_entrada": {"altura_inicial": altura_inicial},
                    "resultados": {"velocidad_final": f"{velocidad_final:.4f} m/s"}
                })
            elif tipo_calculo == 'altura_en_tiempo':
                if tiempo is None or tiempo < 0:
                    raise ValueError("Para 'altura_en_tiempo', 'tiempo' debe ser un valor no negativo.")
                if altura_inicial is None or altura_inicial < 0:
                    raise ValueError("Para 'altura_en_tiempo', 'altura_inicial' debe ser un valor no negativo.")
                altura_actual = calcular_altura_en_tiempo(altura_inicial, tiempo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de altura en un tiempo dado en caída libre exitoso.",
                    "parametros_entrada": {"altura_inicial": altura_inicial, "tiempo": tiempo},
                    "resultados": {"altura_actual": f"{altura_actual:.4f} m"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500

@ns_cinematica.route('/tiro-parabolico')
class TiroParabolico(Resource):
    @ns_cinematica.expect(models['tiro_parabolico_model'])
    @ns_cinematica.response(200, 'Success', api.model('TiroParabolicoOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_cinematica.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        velocidad_inicial = data.get('velocidad_inicial')
        angulo_grados = data.get('angulo_grados')
        altura_inicial = data.get('altura_inicial', 0.0)
        tiempo = data.get('tiempo')

        try:
            if velocidad_inicial is None or velocidad_inicial < 0:
                raise ValueError("La velocidad inicial debe ser un valor no negativo.")
            if angulo_grados is None or not (0 <= angulo_grados <= 90):
                raise ValueError("El ángulo de lanzamiento debe estar entre 0 y 90 grados.")
            if altura_inicial is None or altura_inicial < 0:
                raise ValueError("La altura inicial debe ser un valor no negativo.")

            if tipo_calculo == 'tiempo_vuelo':
                tiempo_vuelo = calcular_tiempo_vuelo(velocidad_inicial, angulo_grados, altura_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de tiempo de vuelo exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "angulo_grados": angulo_grados,
                        "altura_inicial": altura_inicial
                    },
                    "resultados": {"tiempo_vuelo": f"{tiempo_vuelo:.4f} s"}
                })
            elif tipo_calculo == 'altura_maxima':
                altura_maxima = calcular_altura_maxima(velocidad_inicial, angulo_grados, altura_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de altura máxima exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "angulo_grados": angulo_grados,
                        "altura_inicial": altura_inicial
                    },
                    "resultados": {"altura_maxima": f"{altura_maxima:.4f} m"}
                })
            elif tipo_calculo == 'alcance_horizontal':
                alcance_horizontal = calcular_alcance_horizontal(velocidad_inicial, angulo_grados, altura_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de alcance horizontal exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "angulo_grados": angulo_grados,
                        "altura_inicial": altura_inicial
                    },
                    "resultados": {"alcance_horizontal": f"{alcance_horizontal:.4f} m"}
                })
            elif tipo_calculo == 'posicion_en_tiempo':
                if tiempo is None or tiempo < 0:
                    raise ValueError("Para 'posicion_en_tiempo', 'tiempo' debe ser un valor no negativo.")
                posicion_x, posicion_y = calcular_posicion_en_tiempo(velocidad_inicial, angulo_grados, tiempo, altura_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de posición en un tiempo dado exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "angulo_grados": angulo_grados,
                        "altura_inicial": altura_inicial,
                        "tiempo": tiempo
                    },
                    "resultados": {"posicion_x": f"{posicion_x:.4f} m", "posicion_y": f"{posicion_y:.4f} m"}
                })
            elif tipo_calculo == 'velocidad_en_tiempo':
                if tiempo is None or tiempo < 0:
                    raise ValueError("Para 'velocidad_en_tiempo', 'tiempo' debe ser un valor no negativo.")
                velocidad_x, velocidad_y = calcular_velocidad_en_tiempo(velocidad_inicial, angulo_grados, tiempo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de velocidad en un tiempo dado exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "angulo_grados": angulo_grados,
                        "tiempo": tiempo
                    },
                    "resultados": {"velocidad_x": f"{velocidad_x:.4f} m/s", "velocidad_y": f"{velocidad_y:.4f} m/s"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_dinamica.route('/plano-inclinado-polea')
class PlanoInclinadoPolea(Resource):
    @ns_dinamica.expect(models['plano_inclinado_polea_model'])
    @ns_dinamica.response(200, 'Success', api.model('PlanoInclinadoPoleaOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_dinamica.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        masa1 = data.get('masa1')
        masa2 = data.get('masa2')
        angulo_inclinacion_grados = data.get('angulo_inclinacion_grados')
        coeficiente_rozamiento_estatico = data.get('coeficiente_rozamiento_estatico')
        coeficiente_rozamiento_cinetico = data.get('coeficiente_rozamiento_cinetico')

        try:
            # Validaciones de entrada
            if masa1 is None or masa1 <= 0:
                raise ValueError("La masa del objeto en el plano (masa1) debe ser un valor positivo.")
            if masa2 is None or masa2 <= 0:
                raise ValueError("La masa del objeto colgante (masa2) debe ser un valor positivo.")
            if angulo_inclinacion_grados is None or not (0 <= angulo_inclinacion_grados <= 90):
                raise ValueError("El ángulo de inclinación debe estar entre 0 y 90 grados.")
            if coeficiente_rozamiento_estatico is None or coeficiente_rozamiento_estatico < 0:
                raise ValueError("El coeficiente de rozamiento estático debe ser un valor no negativo.")
            if coeficiente_rozamiento_cinetico is None or coeficiente_rozamiento_cinetico < 0:
                raise ValueError("El coeficiente de rozamiento cinético debe ser un valor no negativo.")

            # Calcular aceleración y tensión
            aceleracion = calcular_aceleracion_plano_inclinado_polea(
                masa1, masa2, angulo_inclinacion_grados,
                coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico
            )
            tension = calcular_tension(masa1, masa2, angulo_inclinacion_grados, aceleracion)

            return jsonify({
                "success": True,
                "message": "Cálculo de plano inclinado con polea exitoso.",
                "parametros_entrada": {
                    "masa1": masa1,
                    "masa2": masa2,
                    "angulo_inclinacion_grados": angulo_inclinacion_grados,
                    "coeficiente_rozamiento_estatico": coeficiente_rozamiento_estatico,
                    "coeficiente_rozamiento_cinetico": coeficiente_rozamiento_cinetico
                },
                "resultados": {
                    "aceleracion": f"{aceleracion:.4f} m/s²",
                    "tension": f"{tension:.4f} N"
                }
            })
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_cinematica.route('/movimiento-circular-uniforme')
class MovimientoCircularUniforme(Resource):
    @ns_cinematica.expect(models['movimiento_circular_uniforme_model'])
    @ns_cinematica.response(200, 'Success', api.model('MovimientoCircularUniformeOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_cinematica.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        radio = data.get('radio')
        velocidad_angular = data.get('velocidad_angular')
        masa = data.get('masa')

        try:
            if radio is None or radio <= 0:
                raise ValueError("El radio debe ser un valor positivo.")
            if velocidad_angular is None or velocidad_angular < 0:
                raise ValueError("La velocidad angular debe ser un valor no negativo.")

            if tipo_calculo == 'velocidad_tangencial':
                velocidad_tangencial = calcular_velocidad_tangencial(radio, velocidad_angular)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de velocidad tangencial exitoso.",
                    "parametros_entrada": {"radio": radio, "velocidad_angular": velocidad_angular},
                    "resultados": {"velocidad_tangencial": f"{velocidad_tangencial:.4f} m/s"}
                })
            elif tipo_calculo == 'aceleracion_centripeta':
                aceleracion_centripeta = calcular_aceleracion_centripeta(radio, velocidad_angular)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de aceleración centrípeta exitoso.",
                    "parametros_entrada": {"radio": radio, "velocidad_angular": velocidad_angular},
                    "resultados": {"aceleracion_centripeta": f"{aceleracion_centripeta:.4f} m/s²"}
                })
            elif tipo_calculo == 'fuerza_centripeta':
                if masa is None or masa <= 0:
                    raise ValueError("La masa debe ser un valor positivo para calcular la fuerza centrípeta.")
                fuerza_centripeta = calcular_fuerza_centripeta(masa, radio, velocidad_angular)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de fuerza centrípeta exitoso.",
                    "parametros_entrada": {"masa": masa, "radio": radio, "velocidad_angular": velocidad_angular},
                    "resultados": {"fuerza_centripeta": f"{fuerza_centripeta:.4f} N"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_cinematica.route('/pendulo-simple')
class PenduloSimple(Resource):
    @ns_cinematica.expect(models['pendulo_simple_model'])
    @ns_cinematica.response(200, 'Success', api.model('PenduloSimpleOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_cinematica.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        longitud = data.get('longitud')

        try:
            if longitud is None or longitud <= 0:
                raise ValueError("La longitud del péndulo debe ser un valor positivo.")

            if tipo_calculo == 'periodo':
                periodo = calcular_periodo_pendulo_simple(longitud)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de período de péndulo simple exitoso.",
                    "parametros_entrada": {"longitud": longitud},
                    "resultados": {"periodo": f"{periodo:.4f} s"}
                })
            elif tipo_calculo == 'frecuencia':
                frecuencia = calcular_frecuencia_pendulo_simple(longitud)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de frecuencia de péndulo simple exitoso.",
                    "parametros_entrada": {"longitud": longitud},
                    "resultados": {"frecuencia": f"{frecuencia:.4f} Hz"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_cinematica.route('/movimiento-armonico-simple')
class MovimientoArmonicoSimple(Resource):
    @ns_cinematica.expect(models['movimiento_armonico_simple_model'])
    @ns_cinematica.response(200, 'Success', api.model('MovimientoArmonicoSimpleOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_cinematica.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        amplitud = data.get('amplitud')
        frecuencia_angular = data.get('frecuencia_angular')
        tiempo = data.get('tiempo')
        fase_inicial = data.get('fase_inicial', 0.0)
        masa = data.get('masa')
        constante_elastica = data.get('constante_elastica')

        try:
            if amplitud is None or amplitud < 0:
                raise ValueError("La amplitud debe ser un valor no negativo.")
            if frecuencia_angular is None or frecuencia_angular < 0:
                raise ValueError("La frecuencia angular debe ser un valor no negativo.")
            if tiempo is None or tiempo < 0:
                raise ValueError("El tiempo debe ser un valor no negativo.")

            if tipo_calculo == 'posicion':
                posicion = calcular_posicion_mas(amplitud, frecuencia_angular, tiempo, fase_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de posición en MAS exitoso.",
                    "parametros_entrada": {
                        "amplitud": amplitud,
                        "frecuencia_angular": frecuencia_angular,
                        "tiempo": tiempo,
                        "fase_inicial": fase_inicial
                    },
                    "resultados": {"posicion": f"{posicion:.4f} m"}
                })
            elif tipo_calculo == 'velocidad':
                velocidad = calcular_velocidad_mas(amplitud, frecuencia_angular, tiempo, fase_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de velocidad en MAS exitoso.",
                    "parametros_entrada": {
                        "amplitud": amplitud,
                        "frecuencia_angular": frecuencia_angular,
                        "tiempo": tiempo,
                        "fase_inicial": fase_inicial
                    },
                    "resultados": {"velocidad": f"{velocidad:.4f} m/s"}
                })
            elif tipo_calculo == 'aceleracion':
                aceleracion = calcular_aceleracion_mas(amplitud, frecuencia_angular, tiempo, fase_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de aceleración en MAS exitoso.",
                    "parametros_entrada": {
                        "amplitud": amplitud,
                        "frecuencia_angular": frecuencia_angular,
                        "tiempo": tiempo,
                        "fase_inicial": fase_inicial
                    },
                    "resultados": {"aceleracion": f"{aceleracion:.4f} m/s²"}
                })
            elif tipo_calculo == 'periodo_frecuencia':
                if masa is None or masa <= 0:
                    raise ValueError("La masa debe ser un valor positivo para calcular período/frecuencia.")
                if constante_elastica is None or constante_elastica <= 0:
                    raise ValueError("La constante elástica debe ser un valor positivo para calcular período/frecuencia.")
                periodo, frecuencia = calcular_periodo_frecuencia_mas(masa, constante_elastica)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de período y frecuencia en MAS exitoso.",
                    "parametros_entrada": {"masa": masa, "constante_elastica": constante_elastica},
                    "resultados": {"periodo": f"{periodo:.4f} s", "frecuencia": f"{frecuencia:.4f} Hz"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_cinematica.route('/movimiento-rectilineo-uniforme')
class MRU(Resource):
    @ns_cinematica.expect(models['mru_model'])
    @ns_cinematica.response(200, 'Success', api.model('MRUOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_cinematica.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        posicion_inicial = data.get('posicion_inicial')
        velocidad = data.get('velocidad')
        tiempo = data.get('tiempo')
        posicion_final = data.get('posicion_final')

        try:
            if tipo_calculo == 'posicion_final':
                if None in [posicion_inicial, velocidad, tiempo]:
                    raise ValueError("Para calcular la posición final, se requieren posición inicial, velocidad y tiempo.")
                if tiempo < 0:
                    raise ValueError("El tiempo no puede ser negativo.")
                resultado = calcular_posicion_final_mru(posicion_inicial, velocidad, tiempo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de posición final en MRU exitoso.",
                    "parametros_entrada": {
                        "posicion_inicial": posicion_inicial,
                        "velocidad": velocidad,
                        "tiempo": tiempo
                    },
                    "resultados": {"posicion_final": f"{resultado:.4f} m"}
                })
            elif tipo_calculo == 'tiempo':
                if None in [posicion_inicial, velocidad, posicion_final]:
                    raise ValueError("Para calcular el tiempo, se requieren posición inicial, velocidad y posición final.")
                if velocidad == 0:
                    raise ValueError("La velocidad no puede ser cero para calcular el tiempo.")
                resultado = calcular_tiempo_mru(posicion_inicial, velocidad, posicion_final)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de tiempo en MRU exitoso.",
                    "parametros_entrada": {
                        "posicion_inicial": posicion_inicial,
                        "velocidad": velocidad,
                        "posicion_final": posicion_final
                    },
                    "resultados": {"tiempo": f"{resultado:.4f} s"}
                })
            elif tipo_calculo == 'velocidad':
                if None in [posicion_inicial, tiempo, posicion_final]:
                    raise ValueError("Para calcular la velocidad, se requieren posición inicial, tiempo y posición final.")
                if tiempo == 0:
                    raise ValueError("El tiempo no puede ser cero para calcular la velocidad.")
                resultado = calcular_velocidad_mru(posicion_inicial, tiempo, posicion_final)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de velocidad en MRU exitoso.",
                    "parametros_entrada": {
                        "posicion_inicial": posicion_inicial,
                        "tiempo": tiempo,
                        "posicion_final": posicion_final
                    },
                    "resultados": {"velocidad": f"{resultado:.4f} m/s"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_cinematica.route('/movimiento-rectilineo-uniformemente-variado')
class MRUV(Resource):
    @ns_cinematica.expect(models['mruv_model'])
    @ns_cinematica.response(200, 'Success', api.model('MRUVOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_cinematica.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        velocidad_inicial = data.get('velocidad_inicial')
        velocidad_final = data.get('velocidad_final')
        aceleracion = data.get('aceleracion')
        tiempo = data.get('tiempo')
        distancia = data.get('distancia')

        try:
            if tipo_calculo == 'velocidad_final_tiempo':
                if None in [velocidad_inicial, aceleracion, tiempo]:
                    raise ValueError("Para calcular la velocidad final, se requieren velocidad inicial, aceleración y tiempo.")
                resultado = calcular_velocidad_final_tiempo(velocidad_inicial, aceleracion, tiempo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de velocidad final en MRUV exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "aceleracion": aceleracion,
                        "tiempo": tiempo
                    },
                    "resultados": {"velocidad_final": f"{resultado:.4f} m/s"}
                })
            elif tipo_calculo == 'distancia_tiempo':
                if None in [velocidad_inicial, aceleracion, tiempo]:
                    raise ValueError("Para calcular la distancia, se requieren velocidad inicial, aceleración y tiempo.")
                resultado = calcular_distancia_tiempo(velocidad_inicial, aceleracion, tiempo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de distancia en MRUV exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "aceleracion": aceleracion,
                        "tiempo": tiempo
                    },
                    "resultados": {"distancia": f"{resultado:.4f} m"}
                })
            elif tipo_calculo == 'velocidad_final_distancia':
                if None in [velocidad_inicial, aceleracion, distancia]:
                    raise ValueError("Para calcular la velocidad final, se requieren velocidad inicial, aceleración y distancia.")
                resultado = calcular_velocidad_final_distancia(velocidad_inicial, aceleracion, distancia)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de velocidad final en MRUV exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "aceleracion": aceleracion,
                        "distancia": distancia
                    },
                    "resultados": {"velocidad_final": f"{resultado:.4f} m/s"}
                })
            elif tipo_calculo == 'tiempo_velocidad_distancia':
                if None in [velocidad_inicial, velocidad_final, distancia]:
                    raise ValueError("Para calcular el tiempo, se requieren velocidad inicial, velocidad final y distancia.")
                resultado = calcular_tiempo_velocidad_distancia(velocidad_inicial, velocidad_final, distancia)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de tiempo en MRUV exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "velocidad_final": velocidad_final,
                        "distancia": distancia
                    },
                    "resultados": {"tiempo": f"{resultado:.4f} s"}
                })
            elif tipo_calculo == 'aceleracion_velocidad_tiempo':
                if None in [velocidad_inicial, velocidad_final, tiempo]:
                    raise ValueError("Para calcular la aceleración, se requieren velocidad inicial, velocidad final y tiempo.")
                if tiempo == 0:
                    raise ValueError("El tiempo no puede ser cero para calcular la aceleración.")
                resultado = calcular_aceleracion_velocidad_tiempo(velocidad_inicial, velocidad_final, tiempo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de aceleración en MRUV exitoso.",
                    "parametros_entrada": {
                        "velocidad_inicial": velocidad_inicial,
                        "velocidad_final": velocidad_final,
                        "tiempo": tiempo
                    },
                    "resultados": {"aceleracion": f"{resultado:.4f} m/s²"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_energia.route('/trabajo-energia-cinetica')
class TrabajoEnergiaCinetica(Resource):
    @ns_energia.expect(models['trabajo_energia_cinetica_model'])
    @ns_energia.response(200, 'Success', api.model('TrabajoEnergiaCineticaOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_energia.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        fuerza = data.get('fuerza')
        distancia = data.get('distancia')
        angulo = data.get('angulo')
        masa = data.get('masa')
        velocidad_inicial = data.get('velocidad_inicial')
        velocidad_final = data.get('velocidad_final')

        try:
            if tipo_calculo == 'trabajo_fuerza_distancia':
                if None in [fuerza, distancia, angulo]:
                    raise ValueError("Para calcular el trabajo, se requieren fuerza, distancia y ángulo.")
                trabajo = calcular_trabajo(fuerza, distancia, angulo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de trabajo exitoso.",
                    "parametros_entrada": {
                        "fuerza": fuerza,
                        "distancia": distancia,
                        "angulo": angulo
                    },
                    "resultados": {"trabajo": f"{trabajo:.4f} J"}
                })
            elif tipo_calculo == 'energia_cinetica':
                if None in [masa, velocidad_inicial]:
                    raise ValueError("Para calcular la energía cinética, se requieren masa y velocidad.")
                energia_cinetica = calcular_energia_cinetica(masa, velocidad_inicial)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de energía cinética exitoso.",
                    "parametros_entrada": {
                        "masa": masa,
                        "velocidad": velocidad_inicial
                    },
                    "resultados": {"energia_cinetica": f"{energia_cinetica:.4f} J"}
                })
            elif tipo_calculo == 'teorema_trabajo_energia':
                if None in [masa, velocidad_inicial, velocidad_final]:
                    raise ValueError("Para calcular el trabajo por el teorema de trabajo-energía, se requieren masa, velocidad inicial y velocidad final.")
                trabajo = calcular_trabajo_teorema_energia_cinetica(masa, velocidad_inicial, velocidad_final)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de trabajo por teorema de trabajo-energía exitoso.",
                    "parametros_entrada": {
                        "masa": masa,
                        "velocidad_inicial": velocidad_inicial,
                        "velocidad_final": velocidad_final
                    },
                    "resultados": {"trabajo": f"{trabajo:.4f} J"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_energia.route('/energia-potencial-gravitatoria')
class EnergiaPotencialGravitatoria(Resource):
    @ns_energia.expect(models['energia_potencial_gravitatoria_model'])
    @ns_energia.response(200, 'Success', api.model('EnergiaPotencialGravitatoriaOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_energia.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        masa = data.get('masa')
        altura = data.get('altura')
        gravedad = data.get('gravedad', 9.81)

        try:
            if None in [masa, altura]:
                raise ValueError("Se requieren masa y altura para calcular la energía potencial gravitatoria.")
            if masa < 0 or altura < 0 or gravedad < 0:
                raise ValueError("La masa, altura y gravedad deben ser valores no negativos.")

            energia_potencial = calcular_energia_potencial_gravitatoria(masa, altura, gravedad)
            return jsonify({
                "success": True,
                "message": "Cálculo de energía potencial gravitatoria exitoso.",
                "parametros_entrada": {
                    "masa": masa,
                    "altura": altura,
                    "gravedad": gravedad
                },
                "resultados": {"energia_potencial": f"{energia_potencial:.4f} J"}
            })
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_energia.route('/energia-potencial-elastica')
class EnergiaPotencialElastica(Resource):
    @ns_energia.expect(models['energia_potencial_elastica_model'])
    @ns_energia.response(200, 'Success', api.model('EnergiaPotencialElasticaOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_energia.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        constante_elastica = data.get('constante_elastica')
        deformacion = data.get('deformacion')

        try:
            if None in [constante_elastica, deformacion]:
                raise ValueError("Se requieren la constante elástica y la deformación para calcular la energía potencial elástica.")
            if constante_elastica < 0:
                raise ValueError("La constante elástica debe ser un valor no negativo.")

            energia_potencial = calcular_energia_potencial_elastica(constante_elastica, deformacion)
            return jsonify({
                "success": True,
                "message": "Cálculo de energía potencial elástica exitoso.",
                "parametros_entrada": {
                    "constante_elastica": constante_elastica,
                    "deformacion": deformacion
                },
                "resultados": {"energia_potencial": f"{energia_potencial:.4f} J"}
            })
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/ley-kirchhoff-voltaje')
class LeyKirchhoffVoltaje(Resource):
    @ns_electricidad_magnetismo.expect(models['ley_kirchhoff_voltaje_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('LeyKirchhoffVoltajeOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        voltajes_conocidos = data.get('voltajes_conocidos', [])
        fuentes_voltaje = data.get('fuentes_voltaje', [])

        try:
            if not voltajes_conocidos and not fuentes_voltaje:
                raise ValueError("Debe proporcionar al menos un voltaje conocido o una fuente de voltaje.")

            voltaje_desconocido = calcular_voltaje_desconocido_kirchhoff(voltajes_conocidos, fuentes_voltaje)
            return jsonify({
                "success": True,
                "message": "Cálculo de voltaje desconocido por Ley de Kirchhoff exitoso.",
                "parametros_entrada": {
                    "voltajes_conocidos": voltajes_conocidos,
                    "fuentes_voltaje": fuentes_voltaje
                },
                "resultados": {"voltaje_desconocido": f"{voltaje_desconocido:.4f} V"}
            })
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/ley-kirchhoff-corriente')
class LeyKirchhoffCorriente(Resource):
    @ns_electricidad_magnetismo.expect(models['ley_kirchhoff_corriente_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('LeyKirchhoffCorrienteOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        corrientes_conocidas = data.get('corrientes_conocidas', [])
        fuentes_corriente = data.get('fuentes_corriente', [])

        try:
            if not corrientes_conocidas and not fuentes_corriente:
                raise ValueError("Debe proporcionar al menos una corriente conocida o una fuente de corriente.")

            corriente_desconocida = calcular_corriente_desconocida_kirchhoff(corrientes_conocidas, fuentes_corriente)
            return jsonify({
                "success": True,
                "message": "Cálculo de corriente desconocida por Ley de Kirchhoff exitoso.",
                "parametros_entrada": {
                    "corrientes_conocidas": corrientes_conocidas,
                    "fuentes_corriente": fuentes_corriente
                },
                "resultados": {"corriente_desconocida": f"{corriente_desconocida:.4f} A"}
            })
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/capacitancia')
class Capacitancia(Resource):
    @ns_electricidad_magnetismo.expect(models['capacitancia_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('CapacitanciaOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        carga = data.get('carga')
        voltaje = data.get('voltaje')
        area = data.get('area')
        distancia = data.get('distancia')
        permitividad = data.get('permitividad', 8.854e-12) # Permitividad del vacío

        try:
            if tipo_calculo == 'carga_voltaje':
                if None in [carga, voltaje]:
                    raise ValueError("Para calcular la capacitancia, se requieren carga y voltaje.")
                if voltaje == 0:
                    raise ValueError("El voltaje no puede ser cero para calcular la capacitancia.")
                capacitancia = calcular_capacitancia_carga_voltaje(carga, voltaje)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de capacitancia por carga y voltaje exitoso.",
                    "parametros_entrada": {
                        "carga": carga,
                        "voltaje": voltaje
                    },
                    "resultados": {"capacitancia": f"{capacitancia:.9f} F"}
                })
            elif tipo_calculo == 'placas_paralelas':
                if None in [area, distancia]:
                    raise ValueError("Para calcular la capacitancia de placas paralelas, se requieren área y distancia.")
                if distancia == 0:
                    raise ValueError("La distancia no puede ser cero para calcular la capacitancia.")
                capacitancia = calcular_capacitancia_placas_paralelas(area, distancia, permitividad)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de capacitancia de placas paralelas exitoso.",
                    "parametros_entrada": {
                        "area": area,
                        "distancia": distancia,
                        "permitividad": permitividad
                    },
                    "resultados": {"capacitancia": f"{capacitancia:.9f} F"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/circuito-serie')
class CircuitoSerie(Resource):
    @ns_electricidad_magnetismo.expect(models['circuito_serie_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('CircuitoSerieOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        resistencias = data.get('resistencias')
        voltajes = data.get('voltajes')
        corrientes = data.get('corrientes')

        try:
            if resistencias is None or not isinstance(resistencias, list) or len(resistencias) == 0:
                raise ValueError("Se requiere una lista de resistencias para el cálculo.")
            if any(r < 0 for r in resistencias):
                raise ValueError("Las resistencias no pueden ser negativas.")

            if data.get('tipo_calculo') == 'resistencia_total':
                resistencia_total = calcular_resistencia_total_serie(resistencias)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de resistencia total en circuito serie exitoso.",
                    "parametros_entrada": {"resistencias": resistencias},
                    "resultados": {"resistencia_total": f"{resistencia_total:.4f} Ω"}
                })
            elif data.get('tipo_calculo') == 'voltaje_total':
                if voltajes is None or not isinstance(voltajes, list) or len(voltajes) == 0:
                    raise ValueError("Se requiere una lista de voltajes para el cálculo.")
                voltaje_total = calcular_voltaje_total_serie(voltajes)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de voltaje total en circuito serie exitoso.",
                    "parametros_entrada": {"voltajes": voltajes},
                    "resultados": {"voltaje_total": f"{voltaje_total:.4f} V"}
                })
            elif data.get('tipo_calculo') == 'corriente_total':
                if corrientes is None or not isinstance(corrientes, list) or len(corrientes) == 0:
                    raise ValueError("Se requiere una lista de corrientes para el cálculo.")
                corriente_total = calcular_corriente_total_serie(corrientes)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de corriente total en circuito serie exitoso.",
                    "parametros_entrada": {"corrientes": corrientes},
                    "resultados": {"corriente_total": f"{corriente_total:.4f} A"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/circuito-paralelo')
class CircuitoParalelo(Resource):
    @ns_electricidad_magnetismo.expect(models['circuito_paralelo_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('CircuitoParaleloOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        resistencias = data.get('resistencias')
        voltajes = data.get('voltajes')
        corrientes = data.get('corrientes')

        try:
            if resistencias is None or not isinstance(resistencias, list) or len(resistencias) == 0:
                raise ValueError("Se requiere una lista de resistencias para el cálculo.")
            if any(r <= 0 for r in resistencias):
                raise ValueError("Las resistencias deben ser valores positivos.")

            if data.get('tipo_calculo') == 'resistencia_total':
                resistencia_total = calcular_resistencia_total_paralelo(resistencias)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de resistencia total en circuito paralelo exitoso.",
                    "parametros_entrada": {"resistencias": resistencias},
                    "resultados": {"resistencia_total": f"{resistencia_total:.4f} Ω"}
                })
            elif data.get('tipo_calculo') == 'voltaje_total':
                if voltajes is None or not isinstance(voltajes, list) or len(voltajes) == 0:
                    raise ValueError("Se requiere una lista de voltajes para el cálculo.")
                voltaje_total = calcular_voltaje_total_paralelo(voltajes)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de voltaje total en circuito paralelo exitoso.",
                    "parametros_entrada": {"voltajes": voltajes},
                    "resultados": {"voltaje_total": f"{voltaje_total:.4f} V"}
                })
            elif data.get('tipo_calculo') == 'corriente_total':
                if corrientes is None or not isinstance(corrientes, list) or len(corrientes) == 0:
                    raise ValueError("Se requiere una lista de corrientes para el cálculo.")
                corriente_total = calcular_corriente_total_paralelo(corrientes)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de corriente total en circuito paralelo exitoso.",
                    "parametros_entrada": {"corrientes": corrientes},
                    "resultados": {"corriente_total": f"{corriente_total:.4f} A"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/potencia-electrica')
class PotenciaElectrica(Resource):
    @ns_electricidad_magnetismo.expect(models['potencia_electrica_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('PotenciaElectricaOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        voltaje = data.get('voltaje')
        corriente = data.get('corriente')
        resistencia = data.get('resistencia')

        try:
            if tipo_calculo == 'voltaje_corriente':
                if None in [voltaje, corriente]:
                    raise ValueError("Para calcular la potencia eléctrica, se requieren voltaje y corriente.")
                potencia = calcular_potencia_voltaje_corriente(voltaje, corriente)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de potencia eléctrica por voltaje y corriente exitoso.",
                    "parametros_entrada": {
                        "voltaje": voltaje,
                        "corriente": corriente
                    },
                    "resultados": {"potencia": f"{potencia:.4f} W"}
                })
            elif tipo_calculo == 'corriente_resistencia':
                if None in [corriente, resistencia]:
                    raise ValueError("Para calcular la potencia eléctrica, se requieren corriente y resistencia.")
                potencia = calcular_potencia_corriente_resistencia(corriente, resistencia)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de potencia eléctrica por corriente y resistencia exitoso.",
                    "parametros_entrada": {
                        "corriente": corriente,
                        "resistencia": resistencia
                    },
                    "resultados": {"potencia": f"{potencia:.4f} W"}
                })
            elif tipo_calculo == 'voltaje_resistencia':
                if None in [voltaje, resistencia]:
                    raise ValueError("Para calcular la potencia eléctrica, se requieren voltaje y resistencia.")
                if resistencia == 0:
                    raise ValueError("La resistencia no puede ser cero para calcular la potencia.")
                potencia = calcular_potencia_voltaje_resistencia(voltaje, resistencia)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de potencia eléctrica por voltaje y resistencia exitoso.",
                    "parametros_entrada": {
                        "voltaje": voltaje,
                        "resistencia": resistencia
                    },
                    "resultados": {"potencia": f"{potencia:.4f} W"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/inductancia')
class Inductancia(Resource):
    @ns_electricidad_magnetismo.expect(models['inductancia_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('InductanciaOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        voltaje = data.get('voltaje')
        corriente = data.get('corriente')
        tiempo = data.get('tiempo')
        numero_espiras = data.get('numero_espiras')
        flujo_magnetico = data.get('flujo_magnetico')
        longitud = data.get('longitud')
        area_seccion_transversal = data.get('area_seccion_transversal')
        permeabilidad_vacio = data.get('permeabilidad_vacio', 4 * math.pi * 1e-7) # Permeabilidad del vacío

        try:
            if tipo_calculo == 'voltaje_corriente_tiempo':
                if None in [voltaje, corriente, tiempo]:
                    raise ValueError("Para calcular la inductancia, se requieren voltaje, corriente y tiempo.")
                if tiempo == 0:
                    raise ValueError("El tiempo no puede ser cero para calcular la inductancia.")
                inductancia = calcular_inductancia_voltaje_corriente_tiempo(voltaje, corriente, tiempo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de inductancia por voltaje, corriente y tiempo exitoso.",
                    "parametros_entrada": {
                        "voltaje": voltaje,
                        "corriente": corriente,
                        "tiempo": tiempo
                    },
                    "resultados": {"inductancia": f"{inductancia:.4f} H"}
                })
            elif tipo_calculo == 'espiras_flujo_corriente':
                if None in [numero_espiras, flujo_magnetico, corriente]:
                    raise ValueError("Para calcular la inductancia, se requieren número de espiras, flujo magnético y corriente.")
                if corriente == 0:
                    raise ValueError("La corriente no puede ser cero para calcular la inductancia.")
                inductancia = calcular_inductancia_espiras_flujo_corriente(numero_espiras, flujo_magnetico, corriente)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de inductancia por espiras, flujo y corriente exitoso.",
                    "parametros_entrada": {
                        "numero_espiras": numero_espiras,
                        "flujo_magnetico": flujo_magnetico,
                        "corriente": corriente
                    },
                    "resultados": {"inductancia": f"{inductancia:.4f} H"}
                })
            elif tipo_calculo == 'solenoide':
                if None in [numero_espiras, area_seccion_transversal, longitud]:
                    raise ValueError("Para calcular la inductancia de un solenoide, se requieren número de espiras, área de sección transversal y longitud.")
                if longitud == 0:
                    raise ValueError("La longitud no puede ser cero para calcular la inductancia.")
                inductancia = calcular_inductancia_solenoide(numero_espiras, area_seccion_transversal, longitud, permeabilidad_vacio)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de inductancia de un solenoide exitoso.",
                    "parametros_entrada": {
                        "numero_espiras": numero_espiras,
                        "area_seccion_transversal": area_seccion_transversal,
                        "longitud": longitud,
                        "permeabilidad_vacio": permeabilidad_vacio
                    },
                    "resultados": {"inductancia": f"{inductancia:.4f} H"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500





@ns_electricidad_magnetismo.route('/potencial-electrico')
class PotencialElectrico(Resource):
    @ns_electricidad_magnetismo.expect(models['potencial_electrico_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('PotencialElectricoOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        carga = data.get('carga')
        distancia = data.get('distancia')
        densidad_lineal_carga = data.get('densidad_lineal_carga')
        longitud = data.get('longitud')
        densidad_superficial_carga = data.get('densidad_superficial_carga')
        area = data.get('area')
        densidad_volumetrica_carga = data.get('densidad_volumetrica_carga')
        volumen = data.get('volumen')
        constante_k = data.get('constante_k', 8.9875e9)  # Constante de Coulomb

        try:
            if tipo_calculo == 'punto':
                if None in [carga, distancia]:
                    raise ValueError("Para calcular el potencial eléctrico de una carga puntual, se requieren carga y distancia.")
                if distancia == 0:
                    raise ValueError("La distancia no puede ser cero para calcular el potencial eléctrico de una carga puntual.")
                potencial = calcular_potencial_electrico_carga_distancia(carga, distancia, constante_k)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de potencial eléctrico de carga puntual exitoso.",
                    "parametros_entrada": {
                        "carga": carga,
                        "distancia": distancia
                    },
                    "resultados": {"potencial_electrico": f"{potencial:.4f} V"}
                })
            elif tipo_calculo == 'distribucion_lineal':
                if None in [densidad_lineal_carga, longitud, distancia]:
                    raise ValueError("Para calcular el potencial eléctrico de una distribución lineal, se requieren densidad de carga lineal, longitud y distancia.")
                if distancia == 0:
                    raise ValueError("La distancia no puede ser cero para calcular el potencial eléctrico de una distribución lineal.")
                potencial = calcular_potencial_electrico_distribucion_lineal(densidad_lineal_carga, longitud, distancia, constante_k)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de potencial eléctrico de distribución lineal exitoso.",
                    "parametros_entrada": {
                        "densidad_lineal_carga": densidad_lineal_carga,
                        "longitud": longitud,
                        "distancia": distancia
                    },
                    "resultados": {"potencial_electrico": f"{potencial:.4f} V"}
                })
            elif tipo_calculo == 'distribucion_superficial':
                if None in [densidad_superficial_carga, area, distancia]:
                    raise ValueError("Para calcular el potencial eléctrico de una distribución superficial, se requieren densidad de carga superficial, área y distancia.")
                if distancia == 0:
                    raise ValueError("La distancia no puede ser cero para calcular el potencial eléctrico de una distribución superficial.")
                potencial = calcular_potencial_electrico_distribucion_superficial(densidad_superficial_carga, area, distancia, constante_k)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de potencial eléctrico de distribución superficial exitoso.",
                    "parametros_entrada": {
                        "densidad_superficial_carga": densidad_superficial_carga,
                        "area": area,
                        "distancia": distancia
                    },
                    "resultados": {"potencial_electrico": f"{potencial:.4f} V"}
                })
            elif tipo_calculo == 'distribucion_volumetrica':
                if None in [densidad_volumetrica_carga, volumen, distancia]:
                    raise ValueError("Para calcular el potencial eléctrico de una distribución volumétrica, se requieren densidad de carga volumétrica, volumen y distancia.")
                if distancia == 0:
                    raise ValueError("La distancia no puede ser cero para calcular el potencial eléctrico de una distribución volumétrica.")
                potencial = calcular_potencial_electrico_distribucion_volumetrica(densidad_volumetrica_carga, volumen, distancia, constante_k)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de potencial eléctrico de distribución volumétrica exitoso.",
                    "parametros_entrada": {
                        "densidad_volumetrica_carga": densidad_volumetrica_carga,
                        "volumen": volumen,
                        "distancia": distancia
                    },
                    "resultados": {"potencial_electrico": f"{potencial:.4f} V"}
                })
            elif tipo_calculo == 'energia_carga':
                energia_potencial = data.get('energia_potencial')
                carga_prueba = data.get('carga_prueba')
                if None in [energia_potencial, carga_prueba]:
                    raise ValueError("Para calcular el potencial eléctrico, se requieren energía potencial y carga de prueba.")
                if carga_prueba == 0:
                    raise ValueError("La carga de prueba no puede ser cero para calcular el potencial eléctrico.")
                potencial = calcular_potencial_electrico_energia_carga(energia_potencial, carga_prueba)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de potencial eléctrico por energía y carga de prueba exitoso.",
                    "parametros_entrada": {
                        "energia_potencial": energia_potencial,
                        "carga_prueba": carga_prueba
                    },
                    "resultados": {"potencial_electrico": f"{potencial:.4f} V"}
                })
            elif tipo_calculo == 'energia_potencial_electrica':
                voltaje = data.get('voltaje')
                if None in [carga, voltaje]:
                    raise ValueError("Para calcular la energía potencial eléctrica, se requieren carga y voltaje.")
                energia = calcular_energia_potencial_electrica(carga, voltaje)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de energía potencial eléctrica exitoso.",
                    "parametros_entrada": {
                        "carga": carga,
                        "voltaje": voltaje
                    },
                    "resultados": {"energia_potencial_electrica": f"{energia:.4f} J"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/ley-ohm')
class LeyOhm(Resource):
    @ns_electricidad_magnetismo.expect(models['ley_ohm_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('LeyOhmOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        voltaje = data.get('voltaje')
        corriente = data.get('corriente')
        resistencia = data.get('resistencia')

        try:
            if tipo_calculo == 'voltaje':
                if None in [corriente, resistencia]:
                    raise ValueError("Para calcular el voltaje, se requieren corriente y resistencia.")
                resultado = calcular_voltaje(corriente, resistencia)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de voltaje exitoso.",
                    "parametros_entrada": {
                        "corriente": corriente,
                        "resistencia": resistencia
                    },
                    "resultados": {"voltaje": f"{resultado:.4f} V"}
                })
            elif tipo_calculo == 'corriente':
                if None in [voltaje, resistencia]:
                    raise ValueError("Para calcular la corriente, se requieren voltaje y resistencia.")
                if resistencia == 0:
                    raise ValueError("La resistencia no puede ser cero para calcular la corriente.")
                resultado = calcular_corriente(voltaje, resistencia)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de corriente exitoso.",
                    "parametros_entrada": {
                        "voltaje": voltaje,
                        "resistencia": resistencia
                    },
                    "resultados": {"corriente": f"{resultado:.4f} A"}
                })
            elif tipo_calculo == 'resistencia':
                if None in [voltaje, corriente]:
                    raise ValueError("Para calcular la resistencia, se requieren voltaje y corriente.")
                if corriente == 0:
                    raise ValueError("La corriente no puede ser cero para calcular la resistencia.")
                resultado = calcular_resistencia(voltaje, corriente)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de resistencia exitoso.",
                    "parametros_entrada": {
                        "voltaje": voltaje,
                        "corriente": corriente
                    },
                    "resultados": {"resistencia": f"{resultado:.4f} Ω"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/fuerza-magnetica')
class FuerzaMagnetica(Resource):
    @ns_electricidad_magnetismo.expect(models['fuerza_magnetica_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('FuerzaMagneticaOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        carga = data.get('carga')
        velocidad = data.get('velocidad')
        campo_magnetico = data.get('campo_magnetico')
        angulo = data.get('angulo')
        corriente = data.get('corriente')
        longitud = data.get('longitud')

        try:
            if tipo_calculo == 'carga_movil':
                if None in [carga, velocidad, campo_magnetico, angulo]:
                    raise ValueError("Para calcular la fuerza magnética sobre una carga móvil, se requieren carga, velocidad, campo magnético y ángulo.")
                fuerza = calcular_fuerza_magnetica_carga_movil(carga, velocidad, campo_magnetico, angulo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de fuerza magnética sobre carga móvil exitoso.",
                    "parametros_entrada": {
                        "carga": carga,
                        "velocidad": velocidad,
                        "campo_magnetico": campo_magnetico,
                        "angulo": angulo
                    },
                    "resultados": {"fuerza_magnetica": f"{fuerza:.4f} N"}
                })
            elif tipo_calculo == 'conductor':
                if None in [corriente, longitud, campo_magnetico, angulo]:
                    raise ValueError("Para calcular la fuerza magnética sobre un conductor, se requieren corriente, longitud, campo magnético y ángulo.")
                fuerza = calcular_fuerza_magnetica_conductor(corriente, longitud, campo_magnetico, angulo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de fuerza magnética sobre conductor exitoso.",
                    "parametros_entrada": {
                        "corriente": corriente,
                        "longitud": longitud,
                        "campo_magnetico": campo_magnetico,
                        "angulo": angulo
                    },
                    "resultados": {"fuerza_magnetica": f"{fuerza:.4f} N"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/campo-magnetico')
class CampoMagnetico(Resource):
    @ns_electricidad_magnetismo.expect(models['campo_magnetico_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('CampoMagneticoOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        corriente = data.get('corriente')
        distancia = data.get('distancia')
        numero_espiras = data.get('numero_espiras')
        longitud = data.get('longitud')
        permeabilidad_vacio = data.get('permeabilidad_vacio', 4 * math.pi * 1e-7) # Permeabilidad del vacío

        try:
            if tipo_calculo == 'hilo_recto':
                if None in [corriente, distancia]:
                    raise ValueError("Para calcular el campo magnético de un hilo recto, se requieren corriente y distancia.")
                if distancia == 0:
                    raise ValueError("La distancia no puede ser cero para calcular el campo magnético.")
                campo = calcular_campo_magnetico_hilo_recto(corriente, distancia, permeabilidad_vacio)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de campo magnético de un hilo recto exitoso.",
                    "parametros_entrada": {
                        "corriente": corriente,
                        "distancia": distancia
                    },
                    "resultados": {"campo_magnetico": f"{campo:.4f} T"}
                })
            elif tipo_calculo == 'solenoide':
                if None in [corriente, numero_espiras, longitud]:
                    raise ValueError("Para calcular el campo magnético de un solenoide, se requieren corriente, número de espiras y longitud.")
                if longitud == 0:
                    raise ValueError("La longitud no puede ser cero para calcular el campo magnético.")
                campo = calcular_campo_magnetico_solenoide(corriente, numero_espiras, longitud, permeabilidad_vacio)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de campo magnético de un solenoide exitoso.",
                    "parametros_entrada": {
                        "corriente": corriente,
                        "numero_espiras": numero_espiras,
                        "longitud": longitud
                    },
                    "resultados": {"campo_magnetico": f"{campo:.4f} T"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/flujo-magnetico')
class FlujoMagnetico(Resource):
    @ns_electricidad_magnetismo.expect(models['flujo_magnetico_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('FlujoMagneticoOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        campo_magnetico = data.get('campo_magnetico')
        area = data.get('area')
        angulo = data.get('angulo')

        try:
            if None in [campo_magnetico, area, angulo]:
                raise ValueError("Para calcular el flujo magnético, se requieren campo magnético, área y ángulo.")
            flujo = calcular_flujo_magnetico(campo_magnetico, area, angulo)
            return jsonify({
                "success": True,
                "message": "Cálculo de flujo magnético exitoso.",
                "parametros_entrada": {
                    "campo_magnetico": campo_magnetico,
                    "area": area,
                    "angulo": angulo
                },
                "resultados": {"flujo_magnetico": f"{flujo:.4f} Wb"}
            })
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/ley-faraday')
class LeyFaraday(Resource):
    @ns_electricidad_magnetismo.expect(models['ley_faraday_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('LeyFaradayOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        cambio_flujo_magnetico = data.get('cambio_flujo_magnetico')
        cambio_tiempo = data.get('cambio_tiempo')
        numero_espiras = data.get('numero_espiras')

        try:
            if None in [cambio_flujo_magnetico, cambio_tiempo, numero_espiras]:
                raise ValueError("Para calcular la fuerza electromotriz inducida, se requieren cambio de flujo magnético, cambio de tiempo y número de espiras.")
            if cambio_tiempo == 0:
                raise ValueError("El cambio de tiempo no puede ser cero para calcular la fuerza electromotriz inducida.")
            fem_inducida = calcular_fem_inducida_faraday(cambio_flujo_magnetico, cambio_tiempo, numero_espiras)
            return jsonify({
                "success": True,
                "message": "Cálculo de fuerza electromotriz inducida por Ley de Faraday exitoso.",
                "parametros_entrada": {
                    "cambio_flujo_magnetico": cambio_flujo_magnetico,
                    "cambio_tiempo": cambio_tiempo,
                    "numero_espiras": numero_espiras
                },
                "resultados": {"fem_inducida": f"{fem_inducida:.4f} V"}
            })
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_electricidad_magnetismo.route('/ley-gauss')
class LeyGauss(Resource):
    @ns_electricidad_magnetismo.expect(models['ley_gauss_model'])
    @ns_electricidad_magnetismo.response(200, 'Success', api.model('LeyGaussOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_electricidad_magnetismo.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        carga_encerrada = data.get('carga_encerrada')
        epsilon_0 = data.get('epsilon_0', 8.854e-12) # Permitividad del vacío
        campo_electrico = data.get('campo_electrico')
        area = data.get('area')
        angulo = data.get('angulo')

        try:
            if tipo_calculo == 'flujo_electrico_carga':
                if None in [carga_encerrada]:
                    raise ValueError("Para calcular el flujo eléctrico, se requiere la carga encerrada.")
                flujo = calcular_flujo_electrico_ley_gauss(carga_encerrada, epsilon_0)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de flujo eléctrico por Ley de Gauss exitoso.",
                    "parametros_entrada": {
                        "carga_encerrada": carga_encerrada
                    },
                    "resultados": {"flujo_electrico": f"{flujo:.4f} N·m²/C"}
                })
            elif tipo_calculo == 'flujo_electrico_campo_area':
                if None in [campo_electrico, area, angulo]:
                    raise ValueError("Para calcular el flujo eléctrico, se requieren campo eléctrico, área y ángulo.")
                flujo = calcular_flujo_electrico_campo_area(campo_electrico, area, angulo)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de flujo eléctrico por campo y área exitoso.",
                    "parametros_entrada": {
                        "campo_electrico": campo_electrico,
                        "area": area,
                        "angulo": angulo
                    },
                    "resultados": {"flujo_electrico": f"{flujo:.4f} N·m²/C"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


@ns_ondas.route('/ondas-mecanicas')
class OndasMecanicas(Resource):
    @ns_ondas.expect(models['ondas_mecanicas_model'])
    @ns_ondas.response(200, 'Success', api.model('OndasMecanicasOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw,
        'resultados': fields.Raw
    }))
    @ns_ondas.response(400, 'Bad Request', api.model('ErrorOutput', {
        'success': fields.Boolean,
        'message': fields.String,
        'parametros_entrada': fields.Raw
    }))
    def post(self):
        data = api.payload
        tipo_calculo = data.get('tipo_calculo')
        velocidad = data.get('velocidad')
        frecuencia = data.get('frecuencia')
        longitud_onda = data.get('longitud_onda')
        periodo = data.get('periodo')
        tension = data.get('tension')
        densidad_lineal = data.get('densidad_lineal')

        try:
            if tipo_calculo == 'velocidad_onda':
                if None in [frecuencia, longitud_onda]:
                    raise ValueError("Para calcular la velocidad de una onda, se requieren frecuencia y longitud de onda.")
                velocidad_calculada = calcular_velocidad_onda(frecuencia, longitud_onda)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de velocidad de onda exitoso.",
                    "parametros_entrada": {
                        "frecuencia": frecuencia,
                        "longitud_onda": longitud_onda
                    },
                    "resultados": {"velocidad": f"{velocidad_calculada:.4f} m/s"}
                })
            elif tipo_calculo == 'frecuencia_onda':
                if None in [velocidad, longitud_onda]:
                    raise ValueError("Para calcular la frecuencia de una onda, se requieren velocidad y longitud de onda.")
                if longitud_onda == 0:
                    raise ValueError("La longitud de onda no puede ser cero para calcular la frecuencia.")
                frecuencia_calculada = calcular_frecuencia_onda(velocidad, longitud_onda)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de frecuencia de onda exitoso.",
                    "parametros_entrada": {
                        "velocidad": velocidad,
                        "longitud_onda": longitud_onda
                    },
                    "resultados": {"frecuencia": f"{frecuencia_calculada:.4f} Hz"}
                })
            elif tipo_calculo == 'longitud_onda':
                if None in [velocidad, frecuencia]:
                    raise ValueError("Para calcular la longitud de onda, se requieren velocidad y frecuencia.")
                if frecuencia == 0:
                    raise ValueError("La frecuencia no puede ser cero para calcular la longitud de onda.")
                longitud_onda_calculada = calcular_longitud_onda(velocidad, frecuencia)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de longitud de onda exitoso.",
                    "parametros_entrada": {
                        "velocidad": velocidad,
                        "frecuencia": frecuencia
                    },
                    "resultados": {"longitud_onda": f"{longitud_onda_calculada:.4f} m"}
                })
            elif tipo_calculo == 'periodo_onda':
                if None in [frecuencia]:
                    raise ValueError("Para calcular el periodo de una onda, se requiere frecuencia.")
                if frecuencia == 0:
                    raise ValueError("La frecuencia no puede ser cero para calcular el periodo.")
                periodo_calculado = calcular_periodo_onda(frecuencia)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de periodo de onda exitoso.",
                    "parametros_entrada": {
                        "frecuencia": frecuencia
                    },
                    "resultados": {"periodo": f"{periodo_calculado:.4f} s"}
                })
            elif tipo_calculo == 'velocidad_cuerda':
                if None in [tension, densidad_lineal]:
                    raise ValueError("Para calcular la velocidad de una onda en una cuerda, se requieren tensión y densidad lineal.")
                if densidad_lineal == 0:
                    raise ValueError("La densidad lineal no puede ser cero para calcular la velocidad en una cuerda.")
                velocidad_cuerda_calculada = calcular_velocidad_onda_cuerda(tension, densidad_lineal)
                return jsonify({
                    "success": True,
                    "message": "Cálculo de velocidad de onda en una cuerda exitoso.",
                    "parametros_entrada": {
                        "tension": tension,
                        "densidad_lineal": densidad_lineal
                    },
                    "resultados": {"velocidad_cuerda": f"{velocidad_cuerda_calculada:.4f} m/s"}
                })
            else:
                return jsonify({"success": False, "message": "Tipo de cálculo no válido.", "parametros_entrada": data}), 400
        except ValueError as e:
            return jsonify({"success": False, "message": str(e), "parametros_entrada": data}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Ocurrió un error inesperado: {str(e)}", "parametros_entrada": data}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)