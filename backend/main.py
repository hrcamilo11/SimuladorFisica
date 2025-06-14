from flask import Flask, jsonify, request
from flask_cors import CORS

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
app = Flask(__name__)
CORS(app)

# Constantes físicas (si son necesarias, se pueden mover a un archivo de configuración)
GRAVEDAD = 9.81  # m/s^2

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenido a la API de Simulaciones Físicas",
        "available_simulations": [
            {
                "category": "Cinemática",
                "simulations": [
                    {"name": "Caída Libre", "endpoint": "/simulacion/caida-libre"},
                    {"name": "Tiro Parabólico", "endpoint": "/simulacion/tiro-parabolico"},
                    {"name": "Movimiento Circular Uniforme", "endpoint": "/simulacion/movimiento-circular-uniforme"},
                    {"name": "Péndulo Simple", "endpoint": "/simulacion/pendulo-simple"},
                    {"name": "Movimiento Armónico Simple", "endpoint": "/simulacion/movimiento-armonico-simple"},
                    {"name": "Movimiento Rectilíneo Uniforme (MRU)", "endpoint": "/simulacion/mru"},
                    {"name": "Movimiento Rectilíneo Uniformemente Variado (MRUV)", "endpoint": "/simulacion/mruv"}
                ]
            },
            {
                "category": "Colisiones",
                "simulations": [
                    {"name": "Colisión Elástica 1D", "endpoint": "/simulacion/colision-elastica-1d"},
                    {"name": "Colisión Elástica 2D", "endpoint": "/simulacion/colision-elastica-2d"},
                    {"name": "Colisión Elástica 3D", "endpoint": "/simulacion/colision-elastica-3d"},
                    {"name": "Colisión Perfectamente Inelástica 1D", "endpoint": "/simulacion/colision-perfectamente-inelastica-1d"},
                    {"name": "Colisión Perfectamente Inelástica 2D", "endpoint": "/simulacion/colision-perfectamente-inelastica-2d"}
                ]
            },
            {
                "category": "Dinámica",
                "simulations": [
                    {"name": "Fuerzas y Leyes de Newton", "endpoint": "/simulacion/fuerzas-leyes-newton"},
                    {"name": "Plano Inclinado", "endpoint": "/simulacion/plano-inclinado"},
                    {"name": "Plano Inclinado con Polea", "endpoint": "/simulacion/plano-inclinado-polea"}
                ]
            },
            {
                "category": "Energía",
                "simulations": [
                    {"name": "Trabajo y Energía Cinética", "endpoint": "/simulacion/trabajo-energia"},
                    {"name": "Energía Potencial Gravitatoria", "endpoint": "/simulacion/energia-potencial-gravitatoria"},
                    {"name": "Energía Potencial Elástica", "endpoint": "/simulacion/energia-potencial-elastica"}
                ]
            },
            {
                "category": "Electricidad y Magnetismo",
                "simulations": [
                    {"name": "Leyes de Kirchhoff (Voltaje)", "endpoint": "/simulacion/electricidad-y-magnetismo/kirchhoff-voltaje"},
                    {"name": "Leyes de Kirchhoff (Corriente)", "endpoint": "/simulacion/electricidad-y-magnetismo/kirchhoff-corriente"},
                    {"name": "Capacitancia", "endpoint": "/simulacion/electricidad-y-magnetismo/capacitancia"},
                    {"name": "Carga de Capacitor", "endpoint": "/simulacion/electricidad-y-magnetismo/carga-capacitor"},
                    {"name": "Voltaje de Capacitor", "endpoint": "/simulacion/electricidad-y-magnetismo/voltaje-capacitor"},
                    {"name": "Circuito en Serie", "endpoint": "/simulacion/electricidad-y-magnetismo/circuito-serie"},
                    {"name": "Circuito en Paralelo", "endpoint": "/simulacion/electricidad-y-magnetismo/circuito-paralelo"},
                    {"name": "Corriente Total", "endpoint": "/simulacion/electricidad-y-magnetismo/corriente-total"},
                    {"name": "Voltaje Total", "endpoint": "/simulacion/electricidad-y-magnetismo/voltaje-total"},
                    {"name": "Divisor de Voltaje", "endpoint": "/simulacion/electricidad-y-magnetismo/divisor-voltaje"},
                    {"name": "Potencia Eléctrica", "endpoint": "/simulacion/electricidad-y-magnetismo/potencia-electrica"},
                    {"name": "Energía Eléctrica", "endpoint": "/simulacion/electricidad-y-magnetismo/energia-electrica"},
                    {"name": "Caída de Voltaje", "endpoint": "/simulacion/electricidad-y-magnetismo/voltaje-caida"},
                    {"name": "Eficiencia Eléctrica", "endpoint": "/simulacion/electricidad-y-magnetismo/eficiencia-electrica"},
                    {"name": "Inductancia", "endpoint": "/simulacion/electricidad-y-magnetismo/inductancia"},
                    {"name": "Energía en Inductor", "endpoint": "/simulacion/electricidad-y-magnetismo/energia-inductor"},
                    {"name": "Campo Magnético", "endpoint": "/simulacion/electricidad-y-magnetismo/campo-magnetico"},
                    {"name": "Fuerza de Lorentz", "endpoint": "/simulacion/electricidad-y-magnetismo/fuerza-lorentz"},
                    {"name": "Flujo Magnético", "endpoint": "/simulacion/electricidad-y-magnetismo/flujo-magnetico"},
                    {"name": "Ley de Ohm", "endpoint": "/simulacion/electricidad-y-magnetismo/ley-ohm"},
                    {"name": "Potencia Ohm", "endpoint": "/simulacion/electricidad-y-magnetismo/potencia-ohm"},
                    {"name": "Resistencia", "endpoint": "/simulacion/electricidad-y-magnetismo/resistencia"},
                    {"name": "Ley de Faraday", "endpoint": "/simulacion/electricidad-y-magnetismo/ley-faraday"}
                ]
            },
            {
                "category": "Ondas",
                "simulations": [
                    {"name": "Longitud de Onda", "endpoint": "/simulacion/ondas/longitud-onda"},
                    {"name": "Frecuencia de Onda", "endpoint": "/simulacion/ondas/frecuencia-onda"}
                ]
            }
        ]
    })

# Rutas de Cinemática
@app.route('/simulacion/caida-libre', methods=['POST'])
def sim_caida_libre():
    data = request.get_json()
    altura_inicial = data.get('altura_inicial')
    tiempo_total_simulacion = data.get('tiempo_total_simulacion')
    num_puntos = data.get('num_puntos', 100)
    resultado = simular_caida_libre(altura_inicial, tiempo_total_simulacion, num_puntos)
    return jsonify(resultado)

@app.route('/simulacion/tiro-parabolico', methods=['POST'])
def sim_tiro_parabolico():
    data = request.get_json()
    velocidad_inicial = data.get('velocidad_inicial')
    angulo_lanzamiento_grados = data.get('angulo_lanzamiento_grados')
    altura_inicial = data.get('altura_inicial', 0)
    num_puntos = data.get('num_puntos', 100)
    resultado = simular_tiro_parabolico(velocidad_inicial, angulo_lanzamiento_grados, altura_inicial, num_puntos)
    return jsonify(resultado)

@app.route('/simulacion/movimiento-circular-uniforme', methods=['POST'])
def sim_movimiento_circular_uniforme():
    data = request.get_json()
    radio = data.get('radio')
    velocidad_angular = data.get('velocidad_angular')
    velocidad_tangencial = data.get('velocidad_tangencial')
    tiempo_total_simulacion = data.get('tiempo_total_simulacion')
    num_puntos = data.get('num_puntos', 100)
    resultado = simular_movimiento_circular_uniforme(radio, velocidad_angular, velocidad_tangencial, tiempo_total_simulacion, num_puntos)
    return jsonify(resultado)

@app.route('/simulacion/pendulo-simple', methods=['POST'])
def sim_pendulo_simple():
    data = request.get_json()
    longitud = data.get('longitud')
    angulo_inicial_grados = data.get('angulo_inicial_grados')
    tiempo_total_simulacion = data.get('tiempo_total_simulacion')
    num_puntos = data.get('num_puntos', 200)
    resultado = simular_pendulo_simple(longitud, angulo_inicial_grados, tiempo_total_simulacion=tiempo_total_simulacion, num_puntos=num_puntos)
    return jsonify(resultado)

@app.route('/simulacion/movimiento-armonico-simple', methods=['POST'])
def sim_movimiento_armonico_simple():
    data = request.get_json()
    amplitud = data.get('amplitud')
    frecuencia_angular = data.get('frecuencia_angular')
    fase_inicial = data.get('fase_inicial', 0)
    tiempo_total_simulacion = data.get('tiempo_total_simulacion')
    num_puntos = data.get('num_puntos', 100)
    resultado = simular_movimiento_armonico_simple(amplitud, frecuencia_angular, fase_inicial, tiempo_total_simulacion, num_puntos)
    return jsonify(resultado)

@app.route('/simulacion/mru', methods=['POST'])
def sim_mru():
    data = request.get_json()
    posicion_inicial = data.get('posicion_inicial')
    velocidad = data.get('velocidad')
    tiempo_total = data.get('tiempo_total')
    num_puntos = data.get('num_puntos', 100)
    resultado = simular_mru(posicion_inicial, velocidad, tiempo_total, num_puntos)
    return jsonify(resultado)

@app.route('/simulacion/mruv', methods=['POST'])
def sim_mruv():
    data = request.get_json()
    velocidad_inicial = data.get('velocidad_inicial')
    aceleracion = data.get('aceleracion')
    posicion_inicial = data.get('posicion_inicial')
    tiempo_total_simulacion = data.get('tiempo_total_simulacion')
    num_puntos = data.get('num_puntos', 100)
    resultado = simular_mruv(velocidad_inicial, aceleracion, posicion_inicial, tiempo_total_simulacion, num_puntos)
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
    num_puntos = data.get('num_puntos', 100)
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
    num_puntos = data.get('num_puntos', 100)
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
    num_puntos = data.get('num_puntos', 100)
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
    num_puntos = data.get('num_puntos', 100)
    resultado = simular_plano_inclinado_polea(masa1, masa2, angulo_inclinacion_grados, coeficiente_rozamiento_cinetico, tiempo_total_simulacion, num_puntos)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5000)