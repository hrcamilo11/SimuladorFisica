from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource
from schemas import init_schemas

# Importaciones de cinemática
from simulations.cinematica.caida_libre import simular_caida_libre
from simulations.cinematica.tiro_parabolico import simular_tiro_parabolico
from simulations.cinematica.movimiento_circular_uniforme import simular_movimiento_circular_uniforme
from simulations.cinematica.pendulo import simular_pendulo_simple
from simulations.cinematica.movimiento_armonico_simple import simular_movimiento_armonico_simple
from simulations.cinematica.mru import simular_mru
from simulations.cinematica.mruv import simular_mruv

# Importaciones de colisiones
from simulations.colisiones.colision_elastica_1d import simular_colision_elastica_1d
from simulations.colisiones.colision_elastica_2d import simular_colision_elastica_2d
from simulations.colisiones.colision_elastica_3d import simular_colision_elastica_3d
from simulations.colisiones.colision_perfectamente_inelastica_1d import simular_colision_perfectamente_inelastica_1d
from simulations.colisiones.colision_perfectamente_inelastica_2d import simular_colision_perfectamente_inelastica_2d

# Importaciones de dinámica
from simulations.dinamica.leyes_newton import simular_leyes_newton
from simulations.dinamica.plano_inclinado import simular_plano_inclinado
from simulations.dinamica.plano_inclinado_polea import simular_plano_inclinado_polea

# Importaciones de energía
from simulations.energia.trabajo_energia import simular_trabajo_energia_cinetica
from simulations.energia.energia_potencial_gravitatoria import simular_energia_potencial_gravitatoria
from simulations.energia.energia_potencial_elastica import simular_energia_potencial_elastica

# Importaciones de electricidad y magnetismo
from simulations.electricidad_y_magnetismo.leyes_kirchhoff import simular_ley_kirchhoff_voltaje, simular_ley_kirchhoff_corriente
from simulations.electricidad_y_magnetismo.capacitancia import simular_capacitancia
from simulations.electricidad_y_magnetismo.calculos_circuitos import simular_circuito_serie, simular_circuito_paralelo
from simulations.electricidad_y_magnetismo.potencia_electrica import simular_potencia_electrica
from simulations.electricidad_y_magnetismo.inductancia import simular_inductancia
from simulations.electricidad_y_magnetismo.magnetismo import simular_campo_magnetico, simular_flujo_magnetico, simular_fuerza_lorentz, simular_ley_faraday
from simulations.electricidad_y_magnetismo.ley_ohm import simular_ley_ohm
from simulations.electricidad_y_magnetismo.resistencia import simular_resistencia

# Importaciones de ondas
from simulations.ondas.ondas import simular_longitud_onda, simular_frecuencia_onda, simular_velocidad_onda

# Importaciones de ecuaciones cinemáticas
from simulations.cinematica.ecuaciones_cinematicas import (
    calcular_velocidad_final_tiempo,
    calcular_posicion_final_tiempo,
    calcular_velocidad_final_desplazamiento,
    calcular_desplazamiento_velocidades,
    calcular_tiempo_desplazamiento_velocidades,
    calcular_aceleracion_velocidades_tiempo,
    calcular_tiempo_posicion_velocidad_aceleracion,
    calcular_aceleracion_posicion_velocidad_tiempo,
    calcular_posicion_final_velocidad_aceleracion
)
app = Flask(__name__)
CORS(app)

@app.route('/')
def get_available_simulations():
    available_simulations = [
            {
                "category": "Cinemática",
                "simulations": [
                    {"name": "Caída Libre", "path": "/cinematica/caida-libre"},
                    {"name": "Tiro Parabólico", "path": "/simulacion/tiro-parabolico"},
                    {"name": "Movimiento Circular Uniforme", "path": "/simulacion/movimiento-circular-uniforme"},
                    {"name": "Péndulo Simple", "path": "/simulacion/pendulo-simple"},
                    {"name": "Movimiento Armónico Simple", "path": "/simulacion/movimiento-armonico-simple"},
                    {"name": "Movimiento Rectilíneo Uniforme (MRU)", "path": "/simulacion/mru"},
                    {"name": "Movimiento Rectilíneo Uniformemente Variado (MRUV)", "path": "/simulacion/mruv"}
                ]
            },
            {
                "category": "Colisiones",
                "simulations": [
                    {"name": "Colisión Elástica 1D", "path": "/simulacion/colision-elastica-1d"},
                    {"name": "Colisión Elástica 2D", "path": "/simulacion/colision-elastica-2d"},
                    {"name": "Colisión Elástica 3D", "path": "/simulacion/colision-elastica-3d"},
                    {"name": "Colisión Perfectamente Inelástica 1D", "path": "/simulacion/colision-perfectamente-inelastica-1d"},
                    {"name": "Colisión Perfectamente Inelástica 2D", "path": "/simulacion/colision-perfectamente-inelastica-2d"}
                ]
            },
            {
                "category": "Dinámica",
                "simulations": [
                    {"name": "Leyes de Newton", "path": "/simulacion/fuerzas-leyes-newton"},
                    {"name": "Plano Inclinado", "path": "/simulacion/plano-inclinado"},
                    {"name": "Plano Inclinado con Polea", "path": "/simulacion/plano-inclinado-polea"}
                ]
            },
            {
                "category": "Energía",
                "simulations": [
                    {"name": "Trabajo y Energía Cinética", "path": "/simulacion/trabajo-energia-cinetica"},
                    {"name": "Energía Potencial Gravitatoria", "path": "/simulacion/energia-potencial-gravitatoria"},
                    {"name": "Energía Potencial Elástica", "path": "/simulacion/energia-potencial-elastica"}
                ]
            },
            {
                "category": "Electricidad y Magnetismo",
                "simulations": [
                    {"name": "Leyes de Kirchhoff", "path": "/simulacion/leyes-kirchhoff"},
                    {"name": "Capacitancia", "path": "/simulacion/capacitancia"},
                    {"name": "Cálculos de Circuitos", "path": "/simulacion/calculos-circuitos"},
                    {"name": "Potencia Eléctrica", "path": "/simulacion/potencia-electrica"},
                    {"name": "Inductancia", "path": "/simulacion/inductancia"},
                    {"name": "Magnetismo", "path": "/simulacion/magnetismo"},
                    {"name": "Ley de Ohm", "path": "/simulacion/ley-ohm"},
                    {"name": "Resistencia", "path": "/simulacion/resistencia"}
                ]
            },
            {
                "category": "Ondas",
                "simulations": [
                    {"name": "Longitud de Onda", "path": "/simulacion/longitud-onda"},
                    {"name": "Frecuencia de Onda", "path": "/simulacion/frecuencia-onda"},
                    {"name": "Velocidad de Onda", "path": "/simulacion/velocidad-onda"}
                ]
            },
            {
                "category": "Ecuaciones Cinemáticas",
                "simulations": [
                    {"name": "Velocidad Final (t)", "path": "/ecuaciones-cinematicas/velocidad-final-tiempo"},
                    {"name": "Posición Final (t)", "path": "/ecuaciones-cinematicas/posicion-final-tiempo"},
                    {"name": "Velocidad Final (d)", "path": "/ecuaciones-cinematicas/velocidad-final-desplazamiento"},
                    {"name": "Desplazamiento (v,t)", "path": "/simulacion/ecuaciones-cinematicas/desplazamiento-velocidades"},
                    {"name": "Tiempo (d,v)", "path": "/simulacion/ecuaciones-cinematicas/tiempo-desplazamiento-velocidades"},
                    {"name": "Aceleración (v,t)", "path": "/simulacion/ecuaciones-cinematicas/aceleracion-velocidades-tiempo"},
                    {"name": "Tiempo (d,v,a)", "path": "/simulacion/ecuaciones-cinematicas/tiempo-posicion-velocidad-aceleracion"},
                    {"name": "Aceleración (d,v,t)", "path": "/simulacion/ecuaciones-cinematicas/aceleracion-posicion-velocidad-tiempo"},
                    {"name": "Posición Final (v,a)", "path": "/simulacion/ecuaciones-cinematicas/posicion-final-velocidad-aceleracion"}
                ]
            }
        ]
    return jsonify({"available_simulations": available_simulations})

api = Api(app,
          version='1.0',
          title='API de Simulaciones Físicas',
          description='API para simular diversos fenómenos físicos y resolver ecuaciones cinemáticas.',
          doc='/swagger')


# Definición de namespaces
ns_cinematica = api.namespace('cinematica', description='Operaciones de Cinemática')
ns_colisiones = api.namespace('colisiones', description='Operaciones de Colisiones')
ns_dinamica = api.namespace('dinamica', description='Operaciones de Dinámica')
ns_energia = api.namespace('energia', description='Operaciones de Energía')
ns_electricidad_magnetismo = api.namespace('electricidad_magnetismo', description='Operaciones de Electricidad y Magnetismo')
ns_ondas = api.namespace('ondas', description='Operaciones de Ondas')
ns_ecuaciones_cinematicas = api.namespace('ecuaciones_cinematicas', description='Operaciones de Ecuaciones Cinemáticas')

# Constantes físicas (si son necesarias, se pueden mover a un archivo de configuración)
GRAVEDAD = 9.81  # m/s^2


# Inicializar modelos de datos
models = init_schemas(api)

@ns_cinematica.route('/caida-libre')
class CaidaLibre(Resource):
    @ns_cinematica.expect(models['caida_libre_model'])
    def post(self):
        data = api.payload
        altura_inicial = data.get('altura_inicial')
        tiempo_total_simulacion = data.get('tiempo_total_simulacion')
        num_puntos = data.get('num_puntos', 10000)
        resultado = simular_caida_libre(altura_inicial, tiempo_total_simulacion, num_puntos)
        return jsonify(resultado)

@ns_ecuaciones_cinematicas.route('/velocidad-final-tiempo')
class VelocidadFinalTiempo(Resource):
    @ns_ecuaciones_cinematicas.expect(models['velocidad_final_tiempo_model'])
    def post(self):
        data = api.payload
        velocidad_inicial = data.get('velocidad_inicial')
        aceleracion = data.get('aceleracion')
        tiempo = data.get('tiempo')
        if None in [velocidad_inicial, aceleracion, tiempo]:
            return jsonify({"error": "Faltan parámetros: velocidad_inicial, aceleracion, tiempo"}), 400
        resultado = calcular_velocidad_final_tiempo(velocidad_inicial, aceleracion, tiempo)
        return jsonify({"velocidad_final": resultado})

@ns_ecuaciones_cinematicas.route('/posicion-final-tiempo')
class PosicionFinalTiempo(Resource):
    @ns_ecuaciones_cinematicas.expect(posicion_final_tiempo_model)
    def post(self):
        data = api.payload
        posicion_inicial = data.get('posicion_inicial')
        velocidad_inicial = data.get('velocidad_inicial')
        aceleracion = data.get('aceleracion')
        tiempo = data.get('tiempo')
        if None in [posicion_inicial, velocidad_inicial, aceleracion, tiempo]:
            return jsonify({"error": "Faltan parámetros: posicion_inicial, velocidad_inicial, aceleracion, tiempo"}), 400
        resultado = calcular_posicion_final_tiempo(posicion_inicial, velocidad_inicial, aceleracion, tiempo)
        return jsonify({"posicion_final": resultado})

@ns_ecuaciones_cinematicas.route('/velocidad-final-desplazamiento')
class VelocidadFinalDesplazamiento(Resource):
    @ns_ecuaciones_cinematicas.expect(velocidad_final_desplazamiento_model)
    def post(self):
        data = api.payload
        velocidad_inicial = data.get('velocidad_inicial')
        aceleracion = data.get('aceleracion')
        desplazamiento = data.get('desplazamiento')
        if None in [velocidad_inicial, aceleracion, desplazamiento]:
            return jsonify({"error": "Faltan parámetros: velocidad_inicial, aceleracion, desplazamiento"}), 400
        resultado = calcular_velocidad_final_desplazamiento(velocidad_inicial, aceleracion, desplazamiento)
        if resultado is None:
            return jsonify({"error": "No hay solución real para la velocidad final con los parámetros dados."}), 400
        return jsonify({"velocidad_final": resultado})



@ns_ecuaciones_cinematicas.route('/posicion-final-tiempo')
class PosicionFinalTiempo(Resource):
    @ns_ecuaciones_cinematicas.expect(models['posicion_final_tiempo_model'])
    def post(self):
        data = api.payload
        posicion_inicial = data.get('posicion_inicial')
        velocidad_inicial = data.get('velocidad_inicial')
        aceleracion = data.get('aceleracion')
        tiempo = data.get('tiempo')
        if None in [posicion_inicial, velocidad_inicial, aceleracion, tiempo]:
            return jsonify({"error": "Faltan parámetros: posicion_inicial, velocidad_inicial, aceleracion, tiempo"}), 400
        resultado = calcular_posicion_final_tiempo(posicion_inicial, velocidad_inicial, aceleracion, tiempo)
        return jsonify({"posicion_final": resultado})

@ns_ecuaciones_cinematicas.route('/velocidad-final-desplazamiento')
class VelocidadFinalDesplazamiento(Resource):
    @ns_ecuaciones_cinematicas.expect(models['velocidad_final_desplazamiento_model'])
    def post(self):
        data = api.payload
        velocidad_inicial = data.get('velocidad_inicial')
        aceleracion = data.get('aceleracion')
        desplazamiento = data.get('desplazamiento')
        if None in [velocidad_inicial, aceleracion, desplazamiento]:
            return jsonify({"error": "Faltan parámetros: velocidad_inicial, aceleracion, desplazamiento"}), 400
        resultado = calcular_velocidad_final_desplazamiento(velocidad_inicial, aceleracion, desplazamiento)
        if resultado is None:
            return jsonify({"error": "No hay solución real para la velocidad final con los parámetros dados."}), 400
        return jsonify({"velocidad_final": resultado})

@ns_ecuaciones_cinematicas.route('/desplazamiento-velocidades')
class DesplazamientoVelocidades(Resource):
    @ns_ecuaciones_cinematicas.expect(models['desplazamiento_velocidades_model'])
    def post(self):
        data = api.payload
        velocidad_inicial = data.get('velocidad_inicial')
        velocidad_final = data.get('velocidad_final')
        tiempo = data.get('tiempo')
        if None in [velocidad_inicial, velocidad_final, tiempo]:
            return jsonify({"error": "Faltan parámetros: velocidad_inicial, velocidad_final, tiempo"}), 400
        resultado = calcular_desplazamiento_velocidades(velocidad_inicial, velocidad_final, tiempo)
        return jsonify({"desplazamiento": resultado})

@ns_ecuaciones_cinematicas.route('/tiempo-desplazamiento-velocidades')
class TiempoDesplazamientoVelocidades(Resource):
    @ns_ecuaciones_cinematicas.expect(models['tiempo_desplazamiento_velocidades_model'])
    def post(self):
        data = api.payload
        desplazamiento = data.get('desplazamiento')
        velocidad_inicial = data.get('velocidad_inicial')
        velocidad_final = data.get('velocidad_final')
        if None in [desplazamiento, velocidad_inicial, velocidad_final]:
            return jsonify({"error": "Faltan parámetros: desplazamiento, velocidad_inicial, velocidad_final"}), 400
        resultado = calcular_tiempo_desplazamiento_velocidades(desplazamiento, velocidad_inicial, velocidad_final)
        if resultado is None:
            return jsonify({"error": "No se pudo calcular el tiempo (posible división por cero o datos inconsistentes)."}), 400
        return jsonify({"tiempo": resultado})

@ns_ecuaciones_cinematicas.route('/aceleracion-velocidades-tiempo')
class AceleracionVelocidadesTiempo(Resource):
    @ns_ecuaciones_cinematicas.expect(models['aceleracion_velocidades_tiempo_model'])
    def post(self):
        data = api.payload
        velocidad_inicial = data.get('velocidad_inicial')
        velocidad_final = data.get('velocidad_final')
        tiempo = data.get('tiempo')
        if None in [velocidad_inicial, velocidad_final, tiempo]:
            return jsonify({"error": "Faltan parámetros: velocidad_inicial, velocidad_final, tiempo"}), 400
        resultado = calcular_aceleracion_velocidades_tiempo(velocidad_inicial, velocidad_final, tiempo)
        if resultado is None:
            return jsonify({"error": "No se pudo calcular la aceleración (tiempo es cero)."}), 400
        return jsonify({"aceleracion": resultado})

@ns_ecuaciones_cinematicas.route('/tiempo-posicion-velocidad-aceleracion')
class TiempoPosicionVelocidadAceleracion(Resource):
    @ns_ecuaciones_cinematicas.expect(models['tiempo_posicion_velocidad_aceleracion_model'])
    def post(self):
        data = api.payload
        posicion_inicial = data.get('posicion_inicial')
        velocidad_inicial = data.get('velocidad_inicial')
        aceleracion = data.get('aceleracion')
        posicion_final = data.get('posicion_final')
        if None in [posicion_inicial, velocidad_inicial, aceleracion, posicion_final]:
            return jsonify({"error": "Faltan parámetros: posicion_inicial, velocidad_inicial, aceleracion, posicion_final"}), 400
        resultado = calcular_tiempo_posicion_velocidad_aceleracion(posicion_inicial, velocidad_inicial, aceleracion, posicion_final)
        if resultado is None:
            return jsonify({"error": "No hay soluciones reales para el tiempo con los parámetros dados."}), 400
        return jsonify({"tiempo": resultado})

@ns_ecuaciones_cinematicas.route('/aceleracion-posicion-velocidad-tiempo')
class AceleracionPosicionVelocidadTiempo(Resource):
    @ns_ecuaciones_cinematicas.expect(models['aceleracion_posicion_velocidad_tiempo_model'])
    def post(self):
        data = api.payload
        posicion_inicial = data.get('posicion_inicial')
        posicion_final = data.get('posicion_final')
        velocidad_inicial = data.get('velocidad_inicial')
        tiempo = data.get('tiempo')
        if None in [posicion_inicial, posicion_final, velocidad_inicial, tiempo]:
            return jsonify({"error": "Faltan parámetros: posicion_inicial, posicion_final, velocidad_inicial, tiempo"}), 400
        resultado = calcular_aceleracion_posicion_velocidad_tiempo(posicion_inicial, posicion_final, velocidad_inicial, tiempo)
        if resultado is None:
            return jsonify({"error": "No se pudo calcular la aceleración (tiempo es cero)."}), 400
        return jsonify({"aceleracion": resultado})

@ns_ecuaciones_cinematicas.route('/posicion-final-velocidad-aceleracion')
class PosicionFinalVelocidadAceleracion(Resource):
    @ns_ecuaciones_cinematicas.expect(models['posicion_final_velocidad_aceleracion_model'])
    def post(self):
        data = api.payload
        posicion_inicial = data.get('posicion_inicial')
        velocidad_inicial = data.get('velocidad_inicial')
        velocidad_final = data.get('velocidad_final')
        aceleracion = data.get('aceleracion')
        if None in [posicion_inicial, velocidad_inicial, velocidad_final, aceleracion]:
            return jsonify({"error": "Faltan parámetros: posicion_inicial, velocidad_inicial, velocidad_final, aceleracion"}), 400
        resultado = calcular_posicion_final_velocidad_aceleracion(posicion_inicial, velocidad_inicial, velocidad_final, aceleracion)
        if resultado is None:
            return jsonify({"error": "No se pudo calcular la posición final (aceleración es cero)."}), 400
        return jsonify({"posicion_final": resultado})

@ns_cinematica.route('/tiro-parabolico')
class TiroParabolico(Resource):
    @ns_cinematica.expect(models['tiro_parabolico_model'])
    def post(self):
        data = api.payload
        velocidad_inicial = data.get('velocidad_inicial')
        angulo_grados = data.get('angulo_grados')
        altura_inicial = data.get('altura_inicial', 0)
        tiempo_total_simulacion = data.get('tiempo_total_simulacion')
        num_puntos = data.get('num_puntos', 10000)
        resultado = simular_tiro_parabolico(velocidad_inicial, angulo_grados, altura_inicial, tiempo_total_simulacion, num_puntos)
        return jsonify(resultado)

@ns_cinematica.route('/movimiento-circular-uniforme')
class MovimientoCircularUniforme(Resource):
    @ns_cinematica.expect(models['movimiento_circular_uniforme_model'])
    def post(self):
        data = api.payload
        radio = data.get('radio')
        velocidad_angular = data.get('velocidad_angular')
        tiempo_total_simulacion = data.get('tiempo_total_simulacion')
        num_puntos = data.get('num_puntos', 10000)
        resultado = simular_movimiento_circular_uniforme(radio, velocidad_angular, tiempo_total_simulacion, num_puntos)
        return jsonify(resultado)

@ns_cinematica.route('/pendulo-simple')
class PenduloSimple(Resource):
    @ns_cinematica.expect(models['pendulo_simple_model'])
    def post(self):
        data = api.payload
        longitud = data.get('longitud')
        angulo_inicial_grados = data.get('angulo_inicial_grados')
        velocidad_angular_inicial = data.get('velocidad_angular_inicial', 0.0)
        tiempo_total_simulacion = data.get('tiempo_total_simulacion')
        num_puntos = data.get('num_puntos', 10000)
        resultado = simular_pendulo_simple(longitud, angulo_inicial_grados, velocidad_angular_inicial, tiempo_total_simulacion, num_puntos)
        return jsonify(resultado)


@app.route('/simulacion/movimiento-armonico-simple', methods=['POST'])
def sim_movimiento_armonico_simple():
    data = request.get_json()
    amplitud = data.get('amplitud')
    frecuencia_angular = data.get('frecuencia_angular')
    fase_inicial = data.get('fase_inicial', 0)
    tiempo_total_simulacion = data.get('tiempo_total_simulacion')
    num_puntos = data.get('num_puntos', 10000)
    resultado = simular_movimiento_armonico_simple(amplitud, frecuencia_angular, fase_inicial, tiempo_total_simulacion, num_puntos)
    return jsonify(resultado)

@app.route('/simulacion/mru', methods=['POST'])
def sim_mru():
    data = request.get_json()
    posicion_inicial = data.get('posicion_inicial', 0.0) # Default to 0.0 if not provided
    velocidad = data.get('velocidad')
    tiempo_total = data.get('tiempo_total')
    num_puntos = data.get('num_puntos', 10000)
    if None in [posicion_inicial, velocidad, tiempo_total]:
        return jsonify({"error": "Faltan parámetros: posicion_inicial, velocidad, tiempo_total"}), 400
    resultado = simular_mru(posicion_inicial, velocidad, tiempo_total, num_puntos)
    return jsonify(resultado)

@app.route('/simulacion/mruv', methods=['POST'])
def sim_mruv():
    data = request.get_json()
    velocidad_inicial = data.get('velocidad_inicial')
    aceleracion = data.get('aceleracion')
    posicion_inicial = data.get('posicion_inicial', 0.0)
    tiempo_total_simulacion = data.get('tiempo_total_simulacion')
    num_puntos = data.get('num_puntos', 10000)
    if None in [velocidad_inicial, aceleracion, posicion_inicial, tiempo_total_simulacion]:
        return jsonify({"error": "Faltan parámetros: velocidad_inicial, aceleracion, posicion_inicial, tiempo_total_simulacion"}), 400
    resultado = simular_mruv(posicion_inicial, velocidad_inicial, aceleracion, tiempo_total_simulacion, num_puntos)
    return jsonify(resultado)

# Rutas de Colisiones
@app.route('/simulacion/colision-elastica-1d', methods=['POST'])
def sim_colision_elastica_1d():
    data = request.get_json()
    m1 = data.get('m1')
    v1_inicial = data.get('v1_inicial')
    m2 = data.get('m2')
    v2_inicial = data.get('v2_inicial')
    resultado = simular_colision_elastica_1d(m1, v1_inicial, m2, v2_inicial)
    return jsonify(resultado)

@app.route('/simulacion/colision-elastica-2d', methods=['POST'])
def sim_colision_elastica_2d():
    data = request.get_json()
    m1 = data.get('m1')
    v1ix = data.get('v1ix')
    v1iy = data.get('v1iy')
    m2 = data.get('m2')
    v2ix = data.get('v2ix')
    v2iy = data.get('v2iy')
    nx = data.get('nx')
    ny = data.get('ny')
    resultado = simular_colision_elastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy, nx, ny)
    return jsonify(resultado)

@app.route('/simulacion/colision-elastica-3d', methods=['POST'])
def sim_colision_elastica_3d():
    data = request.get_json()
    m1 = data.get('m1')
    v1i = data.get('v1i')
    m2 = data.get('m2')
    v2i = data.get('v2i')
    n_vec = data.get('n_vec')
    resultado = simular_colision_elastica_3d(m1, v1i, m2, v2i, n_vec)
    return jsonify(resultado)

@app.route('/simulacion/colision-perfectamente-inelastica-1d', methods=['POST'])
def sim_colision_perfectamente_inelastica_1d():
    data = request.get_json()
    m1 = data.get('m1')
    v1_inicial = data.get('v1_inicial')
    m2 = data.get('m2')
    v2_inicial = data.get('v2_inicial')
    resultado = simular_colision_perfectamente_inelastica_1d(m1, v1_inicial, m2, v2_inicial)
    return jsonify(resultado)

@app.route('/simulacion/colision-perfectamente-inelastica-2d', methods=['POST'])
def sim_colision_perfectamente_inelastica_2d():
    data = request.get_json()
    m1 = data.get('m1')
    v1ix = data.get('v1ix')
    v1iy = data.get('v1iy')
    m2 = data.get('m2')
    v2ix = data.get('v2ix')
    v2iy = data.get('v2iy')
    resultado = simular_colision_perfectamente_inelastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy)
    return jsonify(resultado)








# Rutas de Dinámica
@app.route('/simulacion/fuerzas-leyes-newton', methods=['POST'])
def sim_fuerzas_leyes_newton():
    data = request.get_json()
    masa = data.get('masa')
    fuerza_aplicada = data.get('fuerza_aplicada')
    angulo_grados = data.get('angulo_grados')
    coeficiente_rozamiento_estatico = data.get('coeficiente_rozamiento_estatico')
    coeficiente_rozamiento_cinetico = data.get('coeficiente_rozamiento_cinetico')
    tiempo_total = data.get('tiempo_total')
    num_puntos = data.get('num_puntos', 10000)
    resultado = simular_leyes_newton(masa, fuerza_aplicada, angulo_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico, tiempo_total, num_puntos)
    return jsonify(resultado)

@app.route('/simulacion/plano-inclinado', methods=['POST'])
def sim_plano_inclinado():
    data = request.get_json()
    masa = data.get('masa')
    angulo_inclinacion_grados = data.get('angulo_inclinacion_grados')
    coeficiente_rozamiento_estatico = data.get('coeficiente_rozamiento_estatico')
    coeficiente_rozamiento_cinetico = data.get('coeficiente_rozamiento_cinetico')
    distancia_plano = data.get('distancia_plano')
    velocidad_inicial = data.get('velocidad_inicial', 0)
    num_puntos = data.get('num_puntos', 10000)
    resultado = simular_plano_inclinado(masa, angulo_inclinacion_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico, distancia_plano, velocidad_inicial, num_puntos)
    return jsonify(resultado)

# Rutas de Energía
@app.route('/simulacion/trabajo-energia', methods=['POST'])
def sim_trabajo_energia():
    data = request.get_json()
    masa = data.get('masa')
    fuerza = data.get('fuerza')
    distancia = data.get('distancia')
    velocidad_inicial = data.get('velocidad_inicial')
    angulo_fuerza_desplazamiento_grados = data.get('angulo_fuerza_desplazamiento_grados')
    resultado = simular_trabajo_energia_cinetica(masa, fuerza, distancia, velocidad_inicial, angulo_fuerza_desplazamiento_grados)
    return jsonify(resultado)

@app.route('/simulacion/energia-potencial-gravitatoria', methods=['POST'])
def sim_energia_potencial_gravitatoria():
    data = request.get_json()
    masa = data.get('masa')
    altura_inicial = data.get('altura_inicial')
    altura_final = data.get('altura_final')
    velocidad_inicial = data.get('velocidad_inicial')
    resultado = simular_energia_potencial_gravitatoria(masa, altura_inicial, altura_final, velocidad_inicial)
    return jsonify(resultado)

@app.route('/simulacion/energia-potencial-elastica', methods=['POST'])
def sim_energia_potencial_elastica():
    data = request.get_json()
    masa = data.get('masa')
    constante_elastica = data.get('constante_elastica')
    amplitud = data.get('amplitud')
    tiempo_total = data.get('tiempo_total')
    num_puntos = data.get('num_puntos', 10000)
    fase_inicial_rad = data.get('fase_inicial_rad', 0)
    resultado = simular_energia_potencial_elastica(masa, constante_elastica, amplitud, tiempo_total, num_puntos, fase_inicial_rad)
    return jsonify(resultado)

# Rutas de Electricidad y Magnetismo
@app.route('/simulacion/electricidad-y-magnetismo/kirchhoff-voltaje', methods=['POST'])
def sim_kirchhoff_voltaje():
    data = request.get_json()
    voltajes = data.get('voltajes')
    resultado = simular_ley_kirchhoff_voltaje(voltajes)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/kirchhoff-corriente', methods=['POST'])
def sim_kirchhoff_corriente():
    data = request.get_json()
    corrientes_entrantes = data.get('corrientes_entrantes')
    corrientes_salientes = data.get('corrientes_salientes')
    resultado = simular_ley_kirchhoff_corriente(corrientes_entrantes, corrientes_salientes)
    return jsonify(resultado)



@app.route('/simulacion/electricidad-y-magnetismo/leyes-kirchhoff-corrientes', methods=['POST'])
def sim_leyes_kirchhoff_corrientes():
    data = request.get_json()
    corrientes_entrantes = data.get('corrientes_entrantes')
    corrientes_salientes = data.get('corrientes_salientes')
    if corrientes_entrantes is None or corrientes_salientes is None or not isinstance(corrientes_entrantes, list) or not isinstance(corrientes_salientes, list):
        return jsonify({"success": False, "message": "Se requieren listas de 'corrientes_entrantes' y 'corrientes_salientes' para la simulación de Ley de Corrientes de Kirchhoff."}), 400
    resultado = simular_ley_kirchhoff_corriente(corrientes_entrantes, corrientes_salientes)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/capacitancia', methods=['POST'])
def sim_capacitancia():
    data = request.get_json()
    carga = data.get('carga')
    voltaje = data.get('voltaje')
    if carga is None or voltaje is None:
        return jsonify({"success": False, "message": "Se requieren 'carga' y 'voltaje' para la simulación de capacitancia."}), 400
    resultado = simular_capacitancia(carga, voltaje)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/carga-capacitor', methods=['POST'])
def sim_carga_capacitor():
    data = request.get_json()
    capacitancia = data.get('capacitancia')
    voltaje = data.get('voltaje')
    if capacitancia is None or voltaje is None:
        return jsonify({"success": False, "message": "Se requieren 'capacitancia' y 'voltaje' para la simulación de carga de capacitor."}), 400
    resultado = simular_carga_capacitor(capacitancia, voltaje)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/voltaje-capacitor', methods=['POST'])
def sim_voltaje_capacitor():
    data = request.get_json()
    carga = data.get('carga')
    capacitancia = data.get('capacitancia')
    if carga is None or capacitancia is None:
        return jsonify({"success": False, "message": "Se requieren 'carga' y 'capacitancia' para la simulación de voltaje de capacitor."}), 400
    resultado = simular_voltaje_capacitor(carga, capacitancia)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/circuito-serie', methods=['POST'])
def sim_circuito_serie():
    data = request.get_json()
    resistencias = data.get('resistencias')
    if resistencias is None or not isinstance(resistencias, list):
        return jsonify({"success": False, "message": "Se requiere una lista de 'resistencias' para la simulación de circuito en serie."}), 400
    resultado = simular_circuito_serie(resistencias)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/circuito-paralelo', methods=['POST'])
def sim_circuito_paralelo():
    data = request.get_json()
    resistencias = data.get('resistencias')
    if resistencias is None or not isinstance(resistencias, list):
        return jsonify({"success": False, "message": "Se requiere una lista de 'resistencias' para la simulación de circuito en paralelo."}), 400
    resultado = simular_circuito_paralelo(resistencias)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/corriente-total', methods=['POST'])
def sim_corriente_total():
    data = request.get_json()
    voltaje_total = data.get('voltaje_total')
    resistencia_total = data.get('resistencia_total')
    if voltaje_total is None or resistencia_total is None:
        return jsonify({"success": False, "message": "Se requieren 'voltaje_total' y 'resistencia_total' para la simulación de corriente total."}), 400
    resultado = simular_corriente_total(voltaje_total, resistencia_total)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/voltaje-total', methods=['POST'])
def sim_voltaje_total():
    data = request.get_json()
    corriente_total = data.get('corriente_total')
    resistencia_total = data.get('resistencia_total')
    if corriente_total is None or resistencia_total is None:
        return jsonify({"success": False, "message": "Se requieren 'corriente_total' y 'resistencia_total' para la simulación de voltaje total."}), 400
    resultado = simular_voltaje_total(corriente_total, resistencia_total)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/divisor-voltaje', methods=['POST'])
def sim_divisor_voltaje():
    data = request.get_json()
    voltaje_fuente = data.get('voltaje_fuente')
    resistencias_serie = data.get('resistencias_serie')
    resistencias_paralelo = data.get('resistencias_paralelo')
    if voltaje_fuente is None or resistencias_serie is None or resistencias_paralelo is None:
        return jsonify({"success": False, "message": "Se requieren 'voltaje_fuente', 'resistencias_serie' y 'resistencias_paralelo' para la simulación de divisor de voltaje."}), 400
    resultado = simular_divisor_voltaje(voltaje_fuente, resistencias_serie, resistencias_paralelo)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/potencia-electrica', methods=['POST'])
def sim_potencia_electrica():
    data = request.get_json()
    voltaje = data.get('voltaje')
    corriente = data.get('corriente')
    if voltaje is None or corriente is None:
        return jsonify({"success": False, "message": "Se requieren 'voltaje' y 'corriente' para la simulación de potencia eléctrica."}), 400
    resultado = simular_potencia_electrica(voltaje, corriente)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/energia-electrica', methods=['POST'])
def sim_energia_electrica():
    data = request.get_json()
    potencia = data.get('potencia')
    tiempo = data.get('tiempo')
    if potencia is None or tiempo is None:
        return jsonify({"success": False, "message": "Se requieren 'potencia' y 'tiempo' para la simulación de energía eléctrica."}), 400
    resultado = simular_energia_electrica(potencia, tiempo)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/voltaje-caida', methods=['POST'])
def sim_voltaje_caida():
    data = request.get_json()
    corriente = data.get('corriente')
    resistencia = data.get('resistencia')
    if corriente is None or resistencia is None:
        return jsonify({"success": False, "message": "Se requieren 'corriente' y 'resistencia' para la simulación de caída de voltaje."}), 400
    resultado = simular_voltaje_caida(corriente, resistencia)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/eficiencia-electrica', methods=['POST'])
def sim_eficiencia_electrica():
    data = request.get_json()
    potencia_salida = data.get('potencia_salida')
    potencia_entrada = data.get('potencia_entrada')
    if potencia_salida is None or potencia_entrada is None:
        return jsonify({"success": False, "message": "Se requieren 'potencia_salida' y 'potencia_entrada' para la simulación de eficiencia eléctrica."}), 400
    resultado = simular_eficiencia_electrica(potencia_salida, potencia_entrada)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/inductancia', methods=['POST'])
def sim_inductancia():
    data = request.get_json()
    flujo_magnetico = data.get('flujo_magnetico')
    corriente = data.get('corriente')
    numero_espiras = data.get('numero_espiras')
    if flujo_magnetico is None or corriente is None or numero_espiras is None:
        return jsonify({"success": False, "message": "Se requieren 'flujo_magnetico', 'corriente' y 'numero_espiras' para la simulación de inductancia."}), 400
    resultado = simular_inductancia(flujo_magnetico, corriente, numero_espiras)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/energia-inductor', methods=['POST'])
def sim_energia_inductor():
    data = request.get_json()
    inductancia = data.get('inductancia')
    corriente = data.get('corriente')
    if inductancia is None or corriente is None:
        return jsonify({"success": False, "message": "Se requieren 'inductancia' y 'corriente' para la simulación de energía en un inductor."}), 400
    resultado = simular_energia_inductor(inductancia, corriente)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/campo-magnetico', methods=['POST'])
def sim_campo_magnetico():
    data = request.get_json()
    corriente = data.get('corriente')
    distancia = data.get('distancia')
    permeabilidad_vacio = data.get('permeabilidad_vacio')
    if corriente is None or distancia is None:
        return jsonify({"success": False, "message": "Se requieren 'corriente' y 'distancia' para la simulación de campo magnético."}), 400
    resultado = simular_campo_magnetico(corriente, distancia, permeabilidad_vacio)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/fuerza-lorentz', methods=['POST'])
def sim_fuerza_lorentz():
    data = request.get_json()
    carga = data.get('carga')
    velocidad = data.get('velocidad')
    campo_magnetico = data.get('campo_magnetico')
    angulo_grados = data.get('angulo_grados')
    if carga is None or velocidad is None or campo_magnetico is None or angulo_grados is None:
        return jsonify({"success": False, "message": "Se requieren 'carga', 'velocidad', 'campo_magnetico' y 'angulo_grados' para la simulación de fuerza de Lorentz."}), 400
    resultado = simular_fuerza_lorentz(carga, velocidad, campo_magnetico, angulo_grados)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/flujo-magnetico', methods=['POST'])
def sim_flujo_magnetico():
    data = request.get_json()
    campo_magnetico = data.get('campo_magnetico')
    area = data.get('area')
    angulo_grados = data.get('angulo_grados')
    if campo_magnetico is None or area is None or angulo_grados is None:
        return jsonify({"success": False, "message": "Se requieren 'campo_magnetico', 'area' y 'angulo_grados' para la simulación de flujo magnético."}), 400
    resultado = simular_flujo_magnetico(campo_magnetico, area, angulo_grados)
    return jsonify(resultado)





@app.route('/simulacion/electricidad-y-magnetismo/ley-ohm', methods=['POST'])
def sim_ley_ohm():
    data = request.get_json()
    voltaje = data.get('voltaje')
    corriente = data.get('corriente')
    resistencia = data.get('resistencia')
    if (voltaje is None and corriente is None) or \
       (voltaje is None and resistencia is None) or \
       (corriente is None and resistencia is None):
        return jsonify({"success": False, "message": "Se requieren al menos dos de los tres parámetros (voltaje, corriente, resistencia) para la simulación de la Ley de Ohm."}), 400
    resultado = simular_ley_ohm(voltaje=voltaje, corriente=corriente, resistencia=resistencia)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/potencia-ohm', methods=['POST'])
def sim_potencia_ohm():
    data = request.get_json()
    voltaje = data.get('voltaje')
    corriente = data.get('corriente')
    resistencia = data.get('resistencia')
    if (voltaje is None and corriente is None and resistencia is None) or \
       (voltaje is not None and corriente is None and resistencia is None) or \
       (corriente is not None and voltaje is None and resistencia is None) or \
       (resistencia is not None and voltaje is None and corriente is None):
        return jsonify({"success": False, "message": "Se requieren al menos dos de los tres parámetros (voltaje, corriente, resistencia) para la simulación de potencia Ohm."}), 400
    resultado = simular_potencia_ohm(voltaje=voltaje, corriente=corriente, resistencia=resistencia)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/resistencia', methods=['POST'])
def sim_resistencia():
    data = request.get_json()
    voltaje = data.get('voltaje')
    corriente = data.get('corriente')
    if voltaje is None or corriente is None:
        return jsonify({"success": False, "message": "Se requieren 'voltaje' y 'corriente' para la simulación de resistencia."}), 400
    resultado = simular_resistencia(voltaje, corriente)
    return jsonify(resultado)



@app.route('/simulacion/ondas/longitud-onda', methods=['POST'])
def sim_longitud_onda():
    data = request.get_json()
    velocidad = data.get('velocidad')
    frecuencia = data.get('frecuencia')
    resultado = simular_longitud_onda(velocidad, frecuencia)
    return jsonify(resultado)

@app.route('/simulacion/ondas/frecuencia-onda', methods=['POST'])
def sim_frecuencia_onda():
    data = request.get_json()
    velocidad = data.get('velocidad')
    longitud_onda = data.get('longitud_onda')
    resultado = simular_frecuencia_onda(velocidad, longitud_onda)
    return jsonify(resultado)

@app.route('/simulacion/ondas/velocidad-onda', methods=['POST'])
def sim_velocidad_onda():
    data = request.get_json()
    frecuencia = data.get('frecuencia')
    longitud_onda = data.get('longitud_onda')
    resultado = simular_velocidad_onda(frecuencia, longitud_onda)
    return jsonify(resultado)

@app.route('/simulacion/electricidad-y-magnetismo/ley-faraday', methods=['POST'])
def sim_ley_faraday():
    data = request.get_json()
    campo_magnetico = data.get('campo_magnetico')
    area = data.get('area')
    angulo_grados = data.get('angulo_grados')
    tiempo = data.get('tiempo')
    if campo_magnetico is None or area is None or angulo_grados is None or tiempo is None:
        return jsonify({"success": False, "message": "Se requieren 'campo_magnetico', 'area', 'angulo_grados' y 'tiempo' para la simulación de la Ley de Faraday."}), 400
    resultado = simular_ley_faraday(campo_magnetico, area, angulo_grados, tiempo)
    return jsonify(resultado)

@app.route('/simulacion/plano-inclinado-polea', methods=['POST'])
def sim_plano_inclinado_polea():
    data = request.get_json()
    masa1 = data.get('masa1')
    masa2 = data.get('masa2')
    angulo_inclinacion_grados = data.get('angulo_inclinacion_grados')
    coeficiente_rozamiento_cinetico = data.get('coeficiente_rozamiento_cinetico')
    tiempo_total_simulacion = data.get('tiempo_total_simulacion')
    num_puntos = data.get('num_puntos', 10000)
    resultado = simular_plano_inclinado_polea(masa1, masa2, angulo_inclinacion_grados, coeficiente_rozamiento_cinetico, tiempo_total_simulacion, num_puntos)
    return jsonify(resultado)

api.add_namespace(ns_cinematica)
api.add_namespace(ns_colisiones)
api.add_namespace(ns_dinamica)
api.add_namespace(ns_energia)
api.add_namespace(ns_electricidad_magnetismo)
api.add_namespace(ns_ondas)
api.add_namespace(ns_ecuaciones_cinematicas)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False, port=5000)