from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app) # Habilitar CORS para todas las rutas

# Constantes físicas
GRAVEDAD = 9.81  # m/s^2

# -------------------- Fórmulas y Lógica de Simulación --------------------

def calcular_caida_libre(altura_inicial, tiempo_total_simulacion=None, num_puntos=100):
    """
    Calcula la posición y velocidad de un objeto en caída libre.
    Si tiempo_total_simulacion no se provee, se calcula hasta que toque el suelo.
    Retorna tiempos, alturas y velocidades.
    """
    if altura_inicial <= 0:
        return [], [], []

    if tiempo_total_simulacion is None:
        # Tiempo para alcanzar el suelo: h = 0.5 * g * t^2 => t = sqrt(2h/g)
        tiempo_hasta_suelo = np.sqrt(2 * altura_inicial / GRAVEDAD)
        tiempo_total_simulacion = tiempo_hasta_suelo

    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    alturas = altura_inicial - 0.5 * GRAVEDAD * tiempos**2
    velocidades = -GRAVEDAD * tiempos # Negativo indica hacia abajo

    # Asegurarse de que la altura no sea negativa y el tiempo no exceda el impacto
    alturas_reales = []
    velocidades_reales = []
    tiempos_reales = []

    for t, h, v in zip(tiempos, alturas, velocidades):
        if h >= 0:
            alturas_reales.append(h)
            velocidades_reales.append(v)
            tiempos_reales.append(t)
        else:
            # Interpolar para encontrar el tiempo exacto de impacto si es necesario
            if not alturas_reales or alturas_reales[-1] > 0: # Solo si no hemos añadido ya el punto de impacto
                # Tiempo para h=0 desde el último punto positivo
                # h_prev - 0.5 * g * (t_impact - t_prev)^2 = 0 ... es más complejo
                # Simplificación: añadir el punto de impacto
                tiempo_impacto_real = np.sqrt(2 * altura_inicial / GRAVEDAD)
                if tiempo_impacto_real > (tiempos_reales[-1] if tiempos_reales else 0):
                     alturas_reales.append(0)
                     velocidades_reales.append(-GRAVEDAD * tiempo_impacto_real)
                     tiempos_reales.append(tiempo_impacto_real)
            break # Detener después del impacto
            
    return tiempos_reales, alturas_reales, velocidades_reales

def calcular_tiro_parabolico(velocidad_inicial, angulo_lanzamiento_grados, altura_inicial=0, num_puntos=100):
    """
    Calcula la trayectoria de un proyectil.
    Retorna tiempos, posiciones_x, posiciones_y.
    """
    if velocidad_inicial <= 0:
        return [], [], []
        
    angulo_lanzamiento_rad = np.deg2rad(angulo_lanzamiento_grados)
    v0x = velocidad_inicial * np.cos(angulo_lanzamiento_rad)
    v0y = velocidad_inicial * np.sin(angulo_lanzamiento_rad)

    # Tiempo total de vuelo (hasta que y vuelva a ser altura_inicial o 0 si altura_inicial es 0)
    # y(t) = y0 + v0y*t - 0.5*g*t^2
    # Si y0 = 0, t_vuelo = 2*v0y/g
    # Si y0 > 0, resolvemos 0 = y0 + v0y*t - 0.5*g*t^2 para t (ecuación cuadrática)
    # at^2 + bt + c = 0  => a = -0.5g, b = v0y, c = y0
    # t = [-b +/- sqrt(b^2 - 4ac)] / 2a
    a = -0.5 * GRAVEDAD
    b = v0y
    c = altura_inicial
    
    discriminante = b**2 - 4*a*c
    if discriminante < 0: # No alcanza el suelo si se lanza hacia arriba desde altura y no tiene suficiente v0y
        # En este caso, calculamos hasta el punto más alto y un poco más
        tiempo_max_altura = v0y / GRAVEDAD
        if tiempo_max_altura <=0: #Lanzado hacia abajo
            tiempo_hasta_suelo_directo = np.sqrt(2 * altura_inicial / GRAVEDAD) if v0y == 0 else (-v0y - np.sqrt(v0y**2 - 4*a*c))/(2*a)
            tiempo_total_simulacion = tiempo_hasta_suelo_directo if tiempo_hasta_suelo_directo > 0 else 1 # fallback
        else:
            tiempo_total_simulacion = tiempo_max_altura * 2 # Estimación simple
    else:
        t1 = (-b + np.sqrt(discriminante)) / (2*a)
        t2 = (-b - np.sqrt(discriminante)) / (2*a)
        tiempo_total_simulacion = max(t1, t2)
        if tiempo_total_simulacion <= 0: # Si el tiempo es negativo o cero, algo anda mal o ya está en el suelo
             # Podría ser que se lanza hacia abajo desde y0. t_vuelo es el positivo.
             tiempo_total_simulacion = t2 if t2 > 0 else (t1 if t1 > 0 else 1) # fallback

    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    posiciones_x = v0x * tiempos
    posiciones_y = altura_inicial + v0y * tiempos - 0.5 * GRAVEDAD * tiempos**2

    # Filtrar puntos después de tocar el suelo (y < 0)
    tiempos_reales = []
    x_reales = []
    y_reales = []
    for t, x, y_pos in zip(tiempos, posiciones_x, posiciones_y):
        if y_pos >= 0:
            tiempos_reales.append(t)
            x_reales.append(x)
            y_reales.append(y_pos)
        else:
            # Interpolar para el punto de impacto exacto
            if not y_reales or y_reales[-1] > 0:
                # y_prev + v0y_prev * dt - 0.5 * g * dt^2 = 0 ... complejo
                # Simplificación: añadir el punto de impacto (y=0)
                # Necesitamos recalcular t para y=0 usando la fórmula cuadrática completa desde el inicio
                # Esto ya se hizo para tiempo_total_simulacion, así que usamos ese tiempo si es el correcto
                if tiempo_total_simulacion > (tiempos_reales[-1] if tiempos_reales else 0):
                    x_impacto = v0x * tiempo_total_simulacion
                    tiempos_reales.append(tiempo_total_simulacion)
                    x_reales.append(x_impacto)
                    y_reales.append(0)
            break
            
    return tiempos_reales, x_reales, y_reales

# -------------------- Endpoints de la API --------------------

@app.route('/')
def home():
    return jsonify({"mensaje": "Backend del Simulador de Física Funcionando!",
                    "simulaciones_disponibles": [
                        {
                            "nombre": "Caída Libre",
                            "descripcion": "Simulación de un objeto en caída libre bajo la gravedad.",
                            "endpoint": "/simulacion/caida-libre"
                        },
                        {
                            "nombre": "Tiro Parabólico",
                            "descripcion": "Simulación de la trayectoria de un proyectil lanzado con un ángulo inicial.",
                            "endpoint": "/simulacion/tiro-parabolico"
                        },
                        {
                            "nombre": "Plano Inclinado",
                            "descripcion": "Simulación del movimiento de un objeto sobre un plano inclinado.",
                            "endpoint": "/simulacion/plano-inclinado"
                        },
                        {
                            "nombre": "Colisión Elástica 1D",
                            "descripcion": "Simulación de colisiones elásticas en una dimensión.",
                            "endpoint": "/simulacion/colision-elastica-1d"
                        },
                        {
                            "nombre": "Colisión Inelástica 1D",
                            "descripcion": "Simulación de colisiones inelásticas en una dimensión.",
                            "endpoint": "/simulacion/colision-inelastica-1d"
                        },
                        {
                            "nombre": "Movimiento Circular Uniforme",
                            "descripcion": "Simulación de un objeto moviéndose en un círculo a velocidad constante.",
                            "endpoint": "/simulacion/movimiento-circular-uniforme"
                        },
                        {
                            "nombre": "Movimiento Armónico Simple",
                            "descripcion": "Simulación de un sistema oscilatorio simple, como un resorte o un péndulo pequeño.",
                            "endpoint": "/simulacion/movimiento-armonico-simple"
                        },
                        {
                            "nombre": "Péndulo Simple",
                            "descripcion": "Simulación del movimiento de un péndulo simple.",
                            "endpoint": "/simulacion/pendulo-simple"
                        },
                        {
                            "nombre": "Colisión Elástica 2D",
                            "descripcion": "Simulación de colisiones elásticas en dos dimensiones.",
                            "endpoint": "/simulacion/colision-elastica-2d"
                        },
                        {
                            "nombre": "Colisión Inelástica 2D",
                            "descripcion": "Simulación de colisiones inelásticas en dos dimensiones.",
                            "endpoint": "/simulacion/colision-inelastica-2d"
                        },
                        {
                            "nombre": "Colisión Elástica 3D",
                            "descripcion": "Simulación de colisiones elásticas en tres dimensiones.",
                            "endpoint": "/simulacion/colision-elastica-3d"
                        },
                        {
                            "nombre": "Colisión Inelástica 3D",
                            "descripcion": "Simulación de colisiones inelásticas en tres dimensiones.",
                            "endpoint": "/simulacion/colision-inelastica-3d"
                        },
                        {
                            "nombre": "Movimiento Rectilíneo Uniforme (MRU)",
                            "descripcion": "Simulación de un objeto moviéndose a velocidad constante en línea recta.",
                            "endpoint": "/simulacion/mru"
                        },
                        {
                            "nombre": "Movimiento Rectilíneo Uniformemente Variado (MRUV)",
                            "descripcion": "Simulación de un objeto moviéndose en línea recta con aceleración constante.",
                            "endpoint": "/simulacion/mruv"
                        },
                        {
                            "nombre": "Fuerzas y Leyes de Newton",
                            "descripcion": "Simulación de la aplicación de fuerzas y sus efectos según las leyes de Newton.",
                            "endpoint": "/simulacion/fuerzas-leyes-newton"
                        },
                        {
                            "nombre": "Trabajo y Energía",
                            "descripcion": "Simulación de conceptos de trabajo realizado por fuerzas y cambios en la energía cinética.",
                            "endpoint": "/simulacion/trabajo-energia"
                        },
                        {
                            "nombre": "Energía Potencial y Conservación",
                            "descripcion": "Simulación de la energía potencial gravitatoria y la conservación de la energía mecánica.",
                            "endpoint": "/simulacion/energia-potencial-conservacion"
                        },
                        {
                            "nombre": "Energía Potencial Elástica",
                            "descripcion": "Simulación de la energía almacenada en un resorte comprimido o estirado.",
                            "endpoint": "/simulacion/energia-potencial-elastica"
                        }
                    ]})

@app.route('/simulacion/caida-libre', methods=['POST'])
def sim_caida_libre():
    data = request.get_json()
    altura_inicial = data.get('altura_inicial')

    if altura_inicial is None:
        return jsonify({"error": "Parámetro 'altura_inicial' es requerido."}), 400
    try:
        altura_inicial = float(altura_inicial)
        if altura_inicial <= 0:
            return jsonify({"error": "'altura_inicial' debe ser un número positivo."}), 400
    except ValueError:
        return jsonify({"error": "'altura_inicial' debe ser un número."}), 400

    tiempos, alturas, velocidades = calcular_caida_libre(altura_inicial)
    
    # Fórmulas utilizadas
    formulas = [
        "h(t) = h0 - (1/2)gt^2",
        "v(t) = -gt",
        f"g = {GRAVEDAD} m/s^2"
    ]

    return jsonify({
        "tipo_simulacion": "Caída Libre",
        "parametros_entrada": {"altura_inicial": altura_inicial},
        "formulas": formulas,
        "resultados": {
            "tiempos_s": list(tiempos),
            "alturas_m": list(alturas),
            "velocidades_mps": list(velocidades)
        }
    })

@app.route('/simulacion/tiro-parabolico', methods=['POST'])
def sim_tiro_parabolico():
    data = request.get_json()
    velocidad_inicial = data.get('velocidad_inicial')
    angulo_lanzamiento = data.get('angulo_lanzamiento_grados')
    altura_inicial = data.get('altura_inicial', 0) # Opcional, por defecto 0

    if velocidad_inicial is None or angulo_lanzamiento is None:
        return jsonify({"error": "Parámetros 'velocidad_inicial' y 'angulo_lanzamiento_grados' son requeridos."}), 400
    
    try:
        velocidad_inicial = float(velocidad_inicial)
        angulo_lanzamiento = float(angulo_lanzamiento)
        altura_inicial = float(altura_inicial)
        if velocidad_inicial <= 0:
            return jsonify({"error": "'velocidad_inicial' debe ser un número positivo."}), 400
        if not (0 <= angulo_lanzamiento <= 90):
             return jsonify({"error": "'angulo_lanzamiento_grados' debe estar entre 0 y 90."}), 400
        if altura_inicial < 0:
            return jsonify({"error": "'altura_inicial' no puede ser negativa."}), 400
    except ValueError:
        return jsonify({"error": "Los parámetros deben ser números."}), 400

    tiempos, posiciones_x, posiciones_y = calcular_tiro_parabolico(velocidad_inicial, angulo_lanzamiento, altura_inicial)

    # Fórmulas utilizadas
    formulas = [
        "x(t) = v0x * t",
        "y(t) = y0 + v0y * t - (1/2)gt^2",
        "v0x = v0 * cos(θ)",
        "v0y = v0 * sin(θ)",
        f"g = {GRAVEDAD} m/s^2"
    ]
    
    return jsonify({
        "tipo_simulacion": "Tiro Parabólico",
        "parametros_entrada": {
            "velocidad_inicial_mps": velocidad_inicial,
            "angulo_lanzamiento_grados": angulo_lanzamiento,
            "altura_inicial_m": altura_inicial
        },
        "formulas": formulas,
        "resultados": {
            "tiempos_s": list(tiempos),
            "posiciones_x_m": list(posiciones_x),
            "posiciones_y_m": list(posiciones_y)
        }
    })

# Aquí se podrían añadir más endpoints para otras simulaciones:
# - Plano Inclinado (con y sin fricción)
# - Colisiones (elásticas e inelásticas, 1D y 2D)
# - Movimiento Circular Uniforme
# - Péndulo Simple

def calcular_plano_inclinado(angulo_inclinacion_grados, longitud_plano, coeficiente_friccion=0, masa=1, num_puntos=100):
    """
    Calcula el movimiento de un objeto en un plano inclinado.
    Retorna tiempos, posiciones_en_plano, velocidades_en_plano.
    """
    if not (0 < angulo_inclinacion_grados < 90):
        return [], [], [] # Ángulo no válido
    if longitud_plano <= 0:
        return [], [], []

    angulo_rad = np.deg2rad(angulo_inclinacion_grados)
    
    # Aceleración debida a la gravedad a lo largo del plano
    ax_gravedad = GRAVEDAD * np.sin(angulo_rad)
    
    # Fuerza normal y fuerza de fricción
    fuerza_normal = masa * GRAVEDAD * np.cos(angulo_rad)
    fuerza_friccion = coeficiente_friccion * fuerza_normal
    
    # Aceleración debida a la fricción (opuesta al movimiento)
    ax_friccion = fuerza_friccion / masa if masa > 0 else 0
    
    # Aceleración neta
    ax_neta = ax_gravedad - ax_friccion
    
    if ax_neta <= 0: # Si la fricción es mayor o igual a la componente de gravedad, no se mueve o se detiene
        # Asumimos que si la aceleración neta es <=0 y parte del reposo, no se mueve.
        # Si tuviera velocidad inicial, sería un caso más complejo de frenado.
        # Por simplicidad, si no hay suficiente para vencer la fricción estática (asumimos cinética aquí), no se mueve.
        tiempos = np.linspace(0, 1, num_puntos) # Simula un corto tiempo en reposo
        posiciones = np.zeros(num_puntos)
        velocidades = np.zeros(num_puntos)
        return list(tiempos), list(posiciones), list(velocidades)

    # Tiempo para recorrer la longitud_plano: s = 0.5 * a * t^2 => t = sqrt(2s/a)
    tiempo_total_simulacion = np.sqrt(2 * longitud_plano / ax_neta)
    
    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    posiciones = 0.5 * ax_neta * tiempos**2
    velocidades = ax_neta * tiempos
    
    # Asegurar que no exceda la longitud del plano
    pos_reales = []
    vel_reales = []
    tiempos_reales = []

    for t, p, v in zip(tiempos, posiciones, velocidades):
        if p <= longitud_plano:
            pos_reales.append(p)
            vel_reales.append(v)
            tiempos_reales.append(t)
        else:
            if not pos_reales or pos_reales[-1] < longitud_plano:
                tiempo_impacto_real = np.sqrt(2 * longitud_plano / ax_neta)
                if tiempo_impacto_real > (tiempos_reales[-1] if tiempos_reales else 0):
                    pos_reales.append(longitud_plano)
                    vel_reales.append(ax_neta * tiempo_impacto_real)
                    tiempos_reales.append(tiempo_impacto_real)
            break
    return tiempos_reales, pos_reales, vel_reales

@app.route('/simulacion/plano-inclinado', methods=['POST'])
def sim_plano_inclinado():
    data = request.get_json()
    angulo_inclinacion = data.get('angulo_inclinacion_grados')
    longitud_plano = data.get('longitud_plano_m')
    coeficiente_friccion = data.get('coeficiente_friccion', 0) # Opcional
    masa = data.get('masa_kg', 1) # Opcional

    if angulo_inclinacion is None or longitud_plano is None:
        return jsonify({"error": "Parámetros 'angulo_inclinacion_grados' y 'longitud_plano_m' son requeridos."}), 400

    try:
        angulo_inclinacion = float(angulo_inclinacion)
        longitud_plano = float(longitud_plano)
        coeficiente_friccion = float(coeficiente_friccion)
        masa = float(masa)

        if not (0 < angulo_inclinacion < 90):
            return jsonify({"error": "'angulo_inclinacion_grados' debe estar entre 0 y 90 (exclusivo)."}), 400
        if longitud_plano <= 0:
            return jsonify({"error": "'longitud_plano_m' debe ser positivo."}), 400
        if coeficiente_friccion < 0:
            return jsonify({"error": "'coeficiente_friccion' no puede ser negativo."}), 400
        if masa <= 0:
            return jsonify({"error": "'masa_kg' debe ser positiva."}), 400
    except ValueError:
        return jsonify({"error": "Todos los parámetros numéricos deben ser números válidos."}), 400

    tiempos, posiciones, velocidades = calcular_plano_inclinado(angulo_inclinacion, longitud_plano, coeficiente_friccion, masa)

    formulas = [
        "ax = g * sin(θ) - μk * g * cos(θ)  (aceleración neta)",
        "s(t) = (1/2) * ax * t^2  (posición si parte del reposo)",
        "v(t) = ax * t  (velocidad si parte del reposo)",
        f"g = {GRAVEDAD} m/s^2",
        "μk es el coeficiente de fricción cinética"
    ]
    if coeficiente_friccion == 0:
        formulas[0] = "ax = g * sin(θ) (sin fricción)"

    return jsonify({
        "tipo_simulacion": "Plano Inclinado",
        "parametros_entrada": {
            "angulo_inclinacion_grados": angulo_inclinacion,
            "longitud_plano_m": longitud_plano,
            "coeficiente_friccion": coeficiente_friccion,
            "masa_kg": masa
        },
        "formulas": formulas,
        "resultados": {
            "tiempos_s": list(tiempos),
            "posiciones_m": list(posiciones),
            "velocidades_mps": list(velocidades)
        }
    })


def calcular_colision_elastica_1d(m1, v1_inicial, m2, v2_inicial):
    """
    Calcula las velocidades finales de dos objetos después de una colisión elástica 1D.
    m1, m2: masas de los objetos.
    v1_inicial, v2_inicial: velocidades iniciales de los objetos.
    Retorna v1_final, v2_final.
    """
    if m1 <= 0 or m2 <= 0:
        # Masas deben ser positivas
        return v1_inicial, v2_inicial # O manejar como error

    # Conservación del momento lineal: m1*v1_i + m2*v2_i = m1*v1_f + m2*v2_f
    # Conservación de la energía cinética (para colisión elástica):
    # (1/2)m1*v1_i^2 + (1/2)m2*v2_i^2 = (1/2)m1*v1_f^2 + (1/2)m2*v2_f^2
    # Resolviendo el sistema de ecuaciones:
    v1_final = ((m1 - m2) / (m1 + m2)) * v1_inicial + ((2 * m2) / (m1 + m2)) * v2_inicial
    v2_final = ((2 * m1) / (m1 + m2)) * v1_inicial + ((m2 - m1) / (m1 + m2)) * v2_inicial
    
    return v1_final, v2_final

@app.route('/simulacion/colision-elastica-1d', methods=['POST'])
def sim_colision_elastica_1d():
    data = request.get_json()
    m1 = data.get('masa1_kg')
    v1_inicial = data.get('velocidad1_inicial_mps')
    m2 = data.get('masa2_kg')
    v2_inicial = data.get('velocidad2_inicial_mps')

    if None in [m1, v1_inicial, m2, v2_inicial]:
        return jsonify({"error": "Parámetros 'masa1_kg', 'velocidad1_inicial_mps', 'masa2_kg', y 'velocidad2_inicial_mps' son requeridos."}), 400

    try:
        m1 = float(m1)
        v1_inicial = float(v1_inicial)
        m2 = float(m2)
        v2_inicial = float(v2_inicial)

        if m1 <= 0 or m2 <= 0:
            return jsonify({"error": "Las masas deben ser positivas."}), 400
    except ValueError:
        return jsonify({"error": "Todos los parámetros deben ser números válidos."}), 400

    v1_final, v2_final = calcular_colision_elastica_1d(m1, v1_inicial, m2, v2_inicial)

    formulas = [
        "Conservación del momento lineal: p_inicial = p_final",
        "m1*v1_i + m2*v2_i = m1*v1_f + m2*v2_f",
        "Conservación de la energía cinética (elástica): K_inicial = K_final",
        "(1/2)m1*v1_i^2 + (1/2)m2*v2_i^2 = (1/2)m1*v1_f^2 + (1/2)m2*v2_f^2",
        "v1_f = ((m1 - m2) / (m1 + m2)) * v1_i + ((2 * m2) / (m1 + m2)) * v2_i",
        "v2_f = ((2 * m1) / (m1 + m2)) * v1_i + ((m2 - m1) / (m1 + m2)) * v2_i"
    ]

    return jsonify({
        "tipo_simulacion": "Colisión Elástica 1D",
        "parametros_entrada": {
            "objeto1": {"masa_kg": m1, "velocidad_inicial_mps": v1_inicial},
            "objeto2": {"masa_kg": m2, "velocidad_inicial_mps": v2_inicial}
        },
        "formulas": formulas,
        "resultados": {
            "objeto1": {"velocidad_final_mps": v1_final},
            "objeto2": {"velocidad_final_mps": v2_final}
        }
    })


def calcular_colision_perfectamente_inelastica_1d(m1, v1_inicial, m2, v2_inicial):
    """
    Calcula la velocidad final común de dos objetos después de una colisión perfectamente inelástica 1D.
    Los objetos quedan unidos después del choque.
    m1, m2: masas de los objetos.
    v1_inicial, v2_inicial: velocidades iniciales de los objetos.
    Retorna v_final_comun.
    """
    if m1 <= 0 or m2 <= 0:
        # Masas deben ser positivas. Podríamos retornar un error o las velocidades iniciales.
        # Para este caso, si las masas no son válidas, no hay colisión significativa para calcular una vf común.
        raise ValueError("Las masas deben ser positivas.")

    # Conservación del momento lineal: m1*v1_i + m2*v2_i = (m1 + m2)*v_f_comun
    v_final_comun = (m1 * v1_inicial + m2 * v2_inicial) / (m1 + m2)
    
    return v_final_comun

@app.route('/simulacion/colision-inelastica-1d', methods=['POST'])
def sim_colision_perfectamente_inelastica_1d():
    data = request.get_json()
    m1 = data.get('masa1_kg')
    v1_inicial = data.get('velocidad1_inicial_mps')
    m2 = data.get('masa2_kg')
    v2_inicial = data.get('velocidad2_inicial_mps')

    if None in [m1, v1_inicial, m2, v2_inicial]:
        return jsonify({"error": "Parámetros 'masa1_kg', 'velocidad1_inicial_mps', 'masa2_kg', y 'velocidad2_inicial_mps' son requeridos."}), 400

    try:
        m1 = float(m1)
        v1_inicial = float(v1_inicial)
        m2 = float(m2)
        v2_inicial = float(v2_inicial)

        if m1 <= 0 or m2 <= 0:
            return jsonify({"error": "Las masas deben ser positivas."}), 400
        
        v_final_comun = calcular_colision_perfectamente_inelastica_1d(m1, v1_inicial, m2, v2_inicial)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500


    formulas = [
        "Conservación del momento lineal: p_inicial = p_final",
        "m1*v1_i + m2*v2_i = (m1 + m2)*vf_comun",
        "vf_comun = (m1*v1_i + m2*v2_i) / (m1 + m2)",
        "En una colisión perfectamente inelástica, los objetos quedan unidos y la energía cinética no se conserva."
    ]

    return jsonify({
        "tipo_simulacion": "Colisión Perfectamente Inelástica 1D",
        "parametros_entrada": {
            "objeto1": {"masa_kg": m1, "velocidad_inicial_mps": v1_inicial},
            "objeto2": {"masa_kg": m2, "velocidad_inicial_mps": v2_inicial}
        },
        "formulas": formulas,
        "resultados": {
            "velocidad_final_comun_mps": v_final_comun
        }
    })


def calcular_movimiento_circular_uniforme(radio, velocidad_angular=None, velocidad_tangencial=None, tiempo_total_simulacion=None, num_puntos=100):
    """
    Calcula la trayectoria de un objeto en Movimiento Circular Uniforme.
    Se debe proveer radio y (velocidad_angular O velocidad_tangencial).
    Si no se da tiempo_total_simulacion, se calcula para una vuelta completa.
    Retorna tiempos, angulos_rad, posiciones_x, posiciones_y, aceleracion_centripeta.
    """
    if radio <= 0:
        raise ValueError("El radio debe ser positivo.")

    if velocidad_angular is None and velocidad_tangencial is None:
        raise ValueError("Se debe proveer velocidad_angular o velocidad_tangencial.")
    if velocidad_angular is not None and velocidad_tangencial is not None:
        # Verificar consistencia si se dan ambas, o priorizar una. Priorizamos angular.
        if not np.isclose(velocidad_tangencial, velocidad_angular * radio):
            # Podríamos recalcular v_t o lanzar error. Por ahora, recalculamos v_t basado en omega.
            velocidad_tangencial = velocidad_angular * radio
            # raise ValueError("Velocidad angular y tangencial inconsistentes.")
    elif velocidad_angular is None:
        if radio == 0: raise ValueError("Radio no puede ser cero si solo se da velocidad tangencial")
        velocidad_angular = velocidad_tangencial / radio
    elif velocidad_tangencial is None:
        velocidad_tangencial = velocidad_angular * radio

    if velocidad_angular == 0: # No hay movimiento circular si omega es 0
        # Podríamos simular un punto estático o devolver error/vacío
        tiempos = np.linspace(0, tiempo_total_simulacion if tiempo_total_simulacion else 1, num_puntos)
        angulos = np.zeros(num_puntos)
        pos_x = np.full(num_puntos, radio) # Asumimos en (r,0) inicialmente
        pos_y = np.zeros(num_puntos)
        return list(tiempos), list(angulos), list(pos_x), list(pos_y), 0.0

    if tiempo_total_simulacion is None:
        # Tiempo para una vuelta completa: T = 2*pi / omega
        if velocidad_angular == 0: tiempo_total_simulacion = 1 # Evitar división por cero, aunque ya cubierto arriba
        else: tiempo_total_simulacion = 2 * np.pi / abs(velocidad_angular)
    
    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    angulos_rad = velocidad_angular * tiempos  # Asumimos ángulo inicial = 0
    
    posiciones_x = radio * np.cos(angulos_rad)
    posiciones_y = radio * np.sin(angulos_rad)
    
    aceleracion_centripeta = (velocidad_tangencial**2) / radio if radio > 0 else 0
    # O también: aceleracion_centripeta = (velocidad_angular**2) * radio

    return list(tiempos), list(angulos_rad), list(posiciones_x), list(posiciones_y), aceleracion_centripeta

@app.route('/simulacion/movimiento-circular-uniforme', methods=['POST'])
def sim_movimiento_circular_uniforme():
    data = request.get_json()
    radio = data.get('radio_m')
    velocidad_angular = data.get('velocidad_angular_rad_s')
    velocidad_tangencial = data.get('velocidad_tangencial_mps')
    tiempo_total = data.get('tiempo_total_s') # Opcional

    if radio is None:
        return jsonify({"error": "Parámetro 'radio_m' es requerido."}), 400
    if velocidad_angular is None and velocidad_tangencial is None:
        return jsonify({"error": "Debe proveer 'velocidad_angular_rad_s' o 'velocidad_tangencial_mps'."}), 400

    try:
        radio = float(radio)
        if radio <= 0:
            return jsonify({"error": "'radio_m' debe ser positivo."}), 400

        v_ang = float(velocidad_angular) if velocidad_angular is not None else None
        v_tan = float(velocidad_tangencial) if velocidad_tangencial is not None else None
        t_total = float(tiempo_total) if tiempo_total is not None else None
        if t_total is not None and t_total <= 0:\
            return jsonify({"error": "'tiempo_total_s' debe ser positivo si se provee."}),400

        tiempos, angulos, xs, ys, ac = calcular_movimiento_circular_uniforme(radio, v_ang, v_tan, t_total)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    # Determinar cuál velocidad se usó para el cálculo final (si ambas fueron dadas)
    final_v_ang = v_tan / radio if v_ang is None and v_tan is not None and radio > 0 else v_ang
    final_v_tan = v_ang * radio if v_tan is None and v_ang is not None else v_tan
    if v_ang is not None and v_tan is not None: # Si ambas se dieron, v_ang tuvo precedencia
        final_v_tan = v_ang * radio

    formulas = [
        "θ(t) = ω * t  (ángulo en función del tiempo, θ0=0)",
        "x(t) = r * cos(θ(t))",
        "y(t) = r * sin(θ(t))",
        "v_t = ω * r  (relación velocidad tangencial y angular)",
        "ac = v_t^2 / r = ω^2 * r  (aceleración centrípeta)",
        "T = 2π / ω  (Período, tiempo para una vuelta)",
        "f = 1 / T = ω / 2π  (Frecuencia)"
    ]

    return jsonify({
        "tipo_simulacion": "Movimiento Circular Uniforme",
        "parametros_entrada": {
            "radio_m": radio,
            "velocidad_angular_rad_s (entrada)": velocidad_angular,
            "velocidad_tangencial_mps (entrada)": velocidad_tangencial,
            "tiempo_total_s (entrada)": tiempo_total
        },
        "parametros_calculados":{
            "velocidad_angular_usada_rad_s": final_v_ang if final_v_ang is not None else (final_v_tan/radio if final_v_tan is not None and radio > 0 else None),
            "velocidad_tangencial_usada_mps": final_v_tan if final_v_tan is not None else (final_v_ang*radio if final_v_ang is not None else None),
            "aceleracion_centripeta_mps2": ac
        },
        "formulas": formulas,
        "resultados": {
            "tiempos_s": list(tiempos),
            "angulos_rad": list(angulos),
            "posiciones_x_m": list(xs),
            "posiciones_y_m": list(ys)
        }
    })


def calcular_movimiento_armonico_simple(amplitud, frecuencia_angular, fase_inicial, tiempo_total_simulacion, num_puntos=100):
    """
    Calcula la posición, velocidad y aceleración de un objeto en Movimiento Armónico Simple.
    x(t) = A * cos(ω*t + φ)
    v(t) = -Aω * sin(ω*t + φ)
    a(t) = -Aω^2 * cos(ω*t + φ) = -ω^2 * x(t)
    """
    if amplitud <= 0:
        raise ValueError("La amplitud debe ser positiva.")
    if frecuencia_angular <= 0:
        raise ValueError("La frecuencia angular (ω) debe ser positiva.")
    if tiempo_total_simulacion <= 0:
        raise ValueError("El tiempo total de simulación debe ser positivo.")

    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    
    posiciones = amplitud * np.cos(frecuencia_angular * tiempos + fase_inicial)
    velocidades = -amplitud * frecuencia_angular * np.sin(frecuencia_angular * tiempos + fase_inicial)
    aceleraciones = -amplitud * (frecuencia_angular**2) * np.cos(frecuencia_angular * tiempos + fase_inicial)
    # Alternativamente: aceleraciones = -(frecuencia_angular**2) * posiciones

    periodo = 2 * np.pi / frecuencia_angular
    frecuencia_hz = 1 / periodo

    return list(tiempos), list(posiciones), list(velocidades), list(aceleraciones), periodo, frecuencia_hz

@app.route('/simulacion/movimiento-armonico-simple', methods=['POST'])
def sim_movimiento_armonico_simple():
    data = request.get_json()
    amplitud = data.get('amplitud_m')
    frecuencia_angular = data.get('frecuencia_angular_rad_s') # ω
    fase_inicial = data.get('fase_inicial_rad', 0.0) # φ, opcional, default 0
    tiempo_total = data.get('tiempo_total_s')

    if amplitud is None or frecuencia_angular is None or tiempo_total is None:
        return jsonify({"error": "Parámetros 'amplitud_m', 'frecuencia_angular_rad_s' y 'tiempo_total_s' son requeridos."}), 400

    try:
        A = float(amplitud)
        omega = float(frecuencia_angular)
        phi = float(fase_inicial)
        t_total = float(tiempo_total)

        if A <= 0: return jsonify({"error": "'amplitud_m' debe ser positiva."}), 400
        if omega <= 0: return jsonify({"error": "'frecuencia_angular_rad_s' debe ser positiva."}), 400
        if t_total <= 0: return jsonify({"error": "'tiempo_total_s' debe ser positivo."}), 400

        tiempos, pos, vel, acel, T, f = calcular_movimiento_armonico_simple(A, omega, phi, t_total)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "x(t) = A * cos(ω*t + φ)  (Posición)",
        "v(t) = -Aω * sin(ω*t + φ)  (Velocidad)",
        "a(t) = -Aω^2 * cos(ω*t + φ) = -ω^2 * x(t)  (Aceleración)",
        "ω = 2πf  (Frecuencia angular)",
        "T = 1/f = 2π/ω  (Período)"
    ]

    return jsonify({
        "tipo_simulacion": "Movimiento Armónico Simple",
        "parametros_entrada": {
            "amplitud_m": A,
            "frecuencia_angular_rad_s": omega,
            "fase_inicial_rad": phi,
            "tiempo_total_s": t_total
        },
        "parametros_calculados": {
            "periodo_s": T,
            "frecuencia_hz": f
        },
        "formulas": formulas,
        "resultados": {
            "tiempos_s": tiempos,
            "posiciones_m": pos,
            "velocidades_mps": vel,
            "aceleraciones_mps2": acel
        }
    })


def calcular_pendulo_simple(longitud, angulo_inicial_rad, gravedad=9.81, tiempo_total_simulacion=None, num_puntos=200):
    """
    Calcula el movimiento de un péndulo simple usando la aproximación de ángulos pequeños (MAS).
    θ(t) = θ_max * cos(ωt + φ)
    ω = sqrt(g/L)
    Si no se da tiempo_total_simulacion, se calcula para dos periodos completos.
    """
    if longitud <= 0:
        raise ValueError("La longitud del péndulo debe ser positiva.")
    if tiempo_total_simulacion is not None and tiempo_total_simulacion <=0:
        raise ValueError("El tiempo total de simulación debe ser positivo si se provee.")
    # Para la aproximación de MAS, el ángulo inicial no debería ser muy grande.
    # No se impone un límite estricto aquí, pero la física es más precisa para |θ_inicial| < ~0.26 rad (15 grados)

    frecuencia_angular = np.sqrt(gravedad / longitud)
    periodo = 2 * np.pi / frecuencia_angular

    if tiempo_total_simulacion is None:
        tiempo_total_simulacion = 2 * periodo # Simular dos periodos por defecto
    
    tiempos = np.linspace(0, tiempo_total_simulacion, num_puntos)
    
    # Asumimos que se suelta desde el reposo en angulo_inicial_rad, entonces φ=0 y θ_max = angulo_inicial_rad
    angulos_rad = angulo_inicial_rad * np.cos(frecuencia_angular * tiempos)
    velocidades_angulares = -angulo_inicial_rad * frecuencia_angular * np.sin(frecuencia_angular * tiempos)
    aceleraciones_angulares = -angulo_inicial_rad * (frecuencia_angular**2) * np.cos(frecuencia_angular * tiempos)
    # O: aceleraciones_angulares = -(frecuencia_angular**2) * angulos_rad

    # Posiciones cartesianas (opcional, pero útil para animación)
    # Origen en el punto de suspensión, y positivo hacia abajo
    pos_x = longitud * np.sin(angulos_rad)
    pos_y = -longitud * np.cos(angulos_rad) # y es negativo (hacia arriba desde el punto más bajo) o positivo (hacia abajo desde el pivote)
                                          # Si el pivote es (0,0), y= -Lcos(theta)

    return list(tiempos), list(angulos_rad), list(velocidades_angulares), list(aceleraciones_angulares), list(pos_x), list(pos_y), periodo, frecuencia_angular

@app.route('/simulacion/pendulo-simple', methods=['POST'])
def sim_pendulo_simple():
    data = request.get_json()
    longitud = data.get('longitud_m')
    angulo_inicial_grados = data.get('angulo_inicial_grados')
    gravedad = data.get('gravedad_mps2', 9.81) # Opcional, default 9.81
    tiempo_total = data.get('tiempo_total_s') # Opcional

    if longitud is None or angulo_inicial_grados is None:
        return jsonify({"error": "Parámetros 'longitud_m' y 'angulo_inicial_grados' son requeridos."}), 400

    try:
        L = float(longitud)
        theta0_deg = float(angulo_inicial_grados)
        g = float(gravedad)
        t_total = float(tiempo_total) if tiempo_total is not None else None

        if L <= 0: return jsonify({"error": "'longitud_m' debe ser positiva."}), 400
        if g <= 0: return jsonify({"error": "'gravedad_mps2' debe ser positiva."}), 400
        if t_total is not None and t_total <=0: return jsonify({"error": "'tiempo_total_s' debe ser positivo si se provee."}), 400
        
        theta0_rad = np.deg2rad(theta0_deg)

        tiempos, ang_rad, vel_ang, acel_ang, xs, ys, T, omega = calcular_pendulo_simple(L, theta0_rad, g, t_total)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "θ(t) = θ_max * cos(ωt + φ) (Aproximación para ángulos pequeños)",
        "ω = sqrt(g/L) (Frecuencia angular)",
        "T = 2π / ω = 2π * sqrt(L/g) (Período)",
        "v_ang(t) = dθ/dt = -θ_max * ω * sin(ωt + φ)",
        "α_ang(t) = d²θ/dt² = -θ_max * ω² * cos(ωt + φ) = -ω² * θ(t)",
        "x(t) = L * sin(θ(t))",
        "y(t) = -L * cos(θ(t)) (desde el punto de suspensión)"
    ]

    return jsonify({
        "tipo_simulacion": "Péndulo Simple (Aprox. Ángulos Pequeños)",
        "parametros_entrada": {
            "longitud_m": L,
            "angulo_inicial_grados": theta0_deg,
            "gravedad_mps2": g,
            "tiempo_total_s (opcional)": t_total
        },
        "parametros_calculados": {
            "angulo_inicial_rad": theta0_rad,
            "frecuencia_angular_rad_s": omega,
            "periodo_s": T
        },
        "formulas": formulas,
        "resultados": {
            "tiempos_s": tiempos,
            "angulos_rad": ang_rad,
            "velocidades_angulares_rad_s": vel_ang,
            "aceleraciones_angulares_rad_s2": acel_ang,
            "posiciones_x_m": xs,
            "posiciones_y_m": ys
        }
    })


def calcular_colision_elastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy, nx, ny):
    """
    Calcula las velocidades finales de dos partículas después de una colisión elástica 2D.
    Se requiere la normal de colisión (nx, ny) como un vector unitario.
    nx, ny: componentes del vector unitario normal a la superficie de contacto, 
            apuntando desde la partícula 1 hacia la partícula 2 si chocan directamente,
            o a lo largo de la línea de acción de la fuerza de colisión.
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")
    
    norm_n = np.sqrt(nx**2 + ny**2)
    if not np.isclose(norm_n, 1.0):
        # Normalize or raise error. Let's normalize for robustness, but ideally input is unit vector.
        # raise ValueError("El vector normal de colisión (nx, ny) debe ser unitario.")
        if norm_n == 0: raise ValueError("El vector normal de colisión no puede ser (0,0).")
        nx /= norm_n
        ny /= norm_n

    # Vector tangente unitario (tx, ty)
    tx = -ny
    ty = nx

    # Velocidades iniciales (vectores)
    v1_i = np.array([v1ix, v1iy])
    v2_i = np.array([v2ix, v2iy])

    # Componentes normales de las velocidades iniciales (escalares)
    v1n_i = v1_i[0] * nx + v1_i[1] * ny  # dot(v1_i, n_vec)
    v2n_i = v2_i[0] * nx + v2_i[1] * ny  # dot(v2_i, n_vec)

    # Componentes tangenciales de las velocidades iniciales (escalares)
    v1t_i = v1_i[0] * tx + v1_i[1] * ty  # dot(v1_i, t_vec)
    v2t_i = v2_i[0] * tx + v2_i[1] * ty  # dot(v2_i, t_vec)

    # Las componentes tangenciales no cambian en una colisión elástica sin fricción
    v1t_f = v1t_i
    v2t_f = v2t_i

    # Las componentes normales cambian según las fórmulas de colisión 1D
    v1n_f = (v1n_i * (m1 - m2) + 2 * m2 * v2n_i) / (m1 + m2)
    v2n_f = (v2n_i * (m2 - m1) + 2 * m1 * v1n_i) / (m1 + m2)

    # Recomponer las velocidades finales vectoriales
    # v1_f = v1n_f * n_vec + v1t_f * t_vec
    v1fx_f = v1n_f * nx + v1t_f * tx
    v1fy_f = v1n_f * ny + v1t_f * ty
    
    # v2_f = v2n_f * n_vec + v2t_f * t_vec
    v2fx_f = v2n_f * nx + v2t_f * tx
    v2fy_f = v2n_f * ny + v2t_f * ty

    return v1fx_f, v1fy_f, v2fx_f, v2fy_f

@app.route('/simulacion/colision-elastica-2d', methods=['POST'])
def sim_colision_elastica_2d():
    data = request.get_json()
    m1 = data.get('m1_kg')
    v1ix = data.get('v1ix_mps')
    v1iy = data.get('v1iy_mps')
    m2 = data.get('m2_kg')
    v2ix = data.get('v2ix_mps')
    v2iy = data.get('v2iy_mps')
    nx = data.get('nx') # Componente x del vector normal de colisión unitario
    ny = data.get('ny') # Componente y del vector normal de colisión unitario

    if None in [m1, v1ix, v1iy, m2, v2ix, v2iy, nx, ny]:
        return jsonify({"error": "Todos los parámetros (m1_kg, v1ix_mps, v1iy_mps, m2_kg, v2ix_mps, v2iy_mps, nx, ny) son requeridos."}), 400

    try:
        m1_f, v1ix_f, v1iy_f = float(m1), float(v1ix), float(v1iy)
        m2_f, v2ix_f, v2iy_f = float(m2), float(v2ix), float(v2iy)
        nx_f, ny_f = float(nx), float(ny)

        if m1_f <= 0 or m2_f <= 0:
            return jsonify({"error": "Las masas deben ser positivas."}), 400
        
        norm_n_check = np.sqrt(nx_f**2 + ny_f**2)
        if not np.isclose(norm_n_check, 1.0):
            # Consider warning or auto-normalizing, but for now strict for unit vector input
            if np.isclose(norm_n_check, 0.0):
                 return jsonify({"error": "El vector normal (nx, ny) no puede ser (0,0)."}), 400
            # Auto-normalize if not unit, could be a policy choice
            # nx_f /= norm_n_check
            # ny_f /= norm_n_check
            # For now, let's be strict and expect a unit vector, or at least non-zero to be normalized by the calc function
            pass # The calculation function will handle normalization or error for non-unit vector if needed


        v1fx, v1fy, v2fx, v2fy = calcular_colision_elastica_2d(m1_f, v1ix_f, v1iy_f, m2_f, v2ix_f, v2iy_f, nx_f, ny_f)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "Conservación del momento lineal (vectorial): m1*v1_i + m2*v2_i = m1*v1_f + m2*v2_f",
        "Conservación de la energía cinética: 0.5*m1*|v1_i|^2 + 0.5*m2*|v2_i|^2 = 0.5*m1*|v1_f|^2 + 0.5*m2*|v2_f|^2",
        "Descomposición de velocidades en componentes normal (n) y tangencial (t) a la línea de impacto.",
        "Componentes tangenciales (perpendiculares a la normal de impacto) no cambian: v1t_f = v1t_i, v2t_f = v2t_i",
        "Componentes normales (a lo largo de la línea de impacto) se transforman como en colisión 1D:",
        "  v1n_f = (v1n_i * (m1 - m2) + 2 * m2 * v2n_i) / (m1 + m2)",
        "  v2n_f = (v2n_i * (m2 - m1) + 2 * m1 * v1n_i) / (m1 + m2)",
        "Vector normal n = (nx, ny), Vector tangente t = (-ny, nx)"
    ]

    return jsonify({
        "tipo_simulacion": "Colisión Elástica 2D",
        "parametros_entrada": {
            "m1_kg": m1_f,
            "v1_inicial_mps": {"x": v1ix_f, "y": v1iy_f},
            "m2_kg": m2_f,
            "v2_inicial_mps": {"x": v2ix_f, "y": v2iy_f},
            "vector_normal_colision": {"nx": nx_f, "ny": ny_f} 
        },
        "formulas": formulas,
        "resultados": {
            "v1_final_mps": {"x": v1fx, "y": v1fy},
            "v2_final_mps": {"x": v2fx, "y": v2fy}
        }
    })


def calcular_colision_perfectamente_inelastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy):
    """
    Calcula la velocidad final común de dos partículas después de una colisión perfectamente inelástica 2D.
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")

    # Conservación del momento lineal en x
    px_total_inicial = m1 * v1ix + m2 * v2ix
    # Conservación del momento lineal en y
    py_total_inicial = m1 * v1iy + m2 * v2iy

    # Masa total después de la colisión
    m_total = m1 + m2

    # Velocidad final común (componentes x e y)
    vfx = px_total_inicial / m_total
    vfy = py_total_inicial / m_total

    return vfx, vfy

@app.route('/simulacion/colision-inelastica-2d', methods=['POST'])
def sim_colision_inelastica_2d():
    data = request.get_json()
    m1 = data.get('m1_kg')
    v1ix = data.get('v1ix_mps')
    v1iy = data.get('v1iy_mps')
    m2 = data.get('m2_kg')
    v2ix = data.get('v2ix_mps')
    v2iy = data.get('v2iy_mps')

    if None in [m1, v1ix, v1iy, m2, v2ix, v2iy]:
        return jsonify({"error": "Todos los parámetros (m1_kg, v1ix_mps, v1iy_mps, m2_kg, v2ix_mps, v2iy_mps) son requeridos."}), 400

    try:
        m1_f, v1ix_f, v1iy_f = float(m1), float(v1ix), float(v1iy)
        m2_f, v2ix_f, v2iy_f = float(m2), float(v2ix), float(v2iy)

        if m1_f <= 0 or m2_f <= 0:
            return jsonify({"error": "Las masas deben ser positivas."}), 400

        vfx, vfy = calcular_colision_perfectamente_inelastica_2d(m1_f, v1ix_f, v1iy_f, m2_f, v2ix_f, v2iy_f)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "Colisión perfectamente inelástica: los objetos se mueven juntos después del impacto.",
        "Conservación del momento lineal (vectorial): P_inicial = P_final",
        "  m1*v1_i + m2*v2_i = (m1 + m2)*v_f",
        "Componente x: m1*v1ix + m2*v2ix = (m1 + m2)*vfx",
        "Componente y: m1*v1iy + m2*v2iy = (m1 + m2)*vfy",
        "  vfx = (m1*v1ix + m2*v2ix) / (m1 + m2)",
        "  vfy = (m1*v1iy + m2*v2iy) / (m1 + m2)",
        "La energía cinética no se conserva (generalmente se pierde)."
    ]

    return jsonify({
        "tipo_simulacion": "Colisión Perfectamente Inelástica 2D",
        "parametros_entrada": {
            "m1_kg": m1_f,
            "v1_inicial_mps": {"x": v1ix_f, "y": v1iy_f},
            "m2_kg": m2_f,
            "v2_inicial_mps": {"x": v2ix_f, "y": v2iy_f}
        },
        "formulas": formulas,
        "resultados": {
            "velocidad_final_comun_mps": {"x": vfx, "y": vfy}
        }
    })


def calcular_colision_elastica_3d(m1, v1i, m2, v2i, n_vec):
    """
    Calcula las velocidades finales de dos partículas después de una colisión elástica 3D.
    v1i, v2i: tuplas o listas de 3 elementos (vx, vy, vz) para las velocidades iniciales.
    n_vec: tupla o lista de 3 elementos (nx, ny, nz) para el vector normal de colisión unitario.
    Retorna (v1fx, v1fy, v1fz), (v2fx, v2fy, v2fz)
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")

    v1i_arr = np.array(v1i)
    v2i_arr = np.array(v2i)
    n_arr = np.array(n_vec)

    norm_n = np.linalg.norm(n_arr)
    if not np.isclose(norm_n, 1.0):
        if np.isclose(norm_n, 0.0): 
            raise ValueError("El vector normal de colisión no puede ser (0,0,0).")
        n_arr = n_arr / norm_n # Normalizar

    # Componentes escalares de las velocidades iniciales a lo largo de la normal n
    v1n_i_scalar = np.dot(v1i_arr, n_arr)
    v2n_i_scalar = np.dot(v2i_arr, n_arr)

    # Componentes vectoriales tangenciales de las velocidades iniciales
    # v_tangencial = v - v_normal_vector = v - dot(v,n)*n
    v1t_i_vec = v1i_arr - v1n_i_scalar * n_arr
    v2t_i_vec = v2i_arr - v2n_i_scalar * n_arr

    # Las componentes tangenciales (vectoriales) no cambian
    v1t_f_vec = v1t_i_vec
    v2t_f_vec = v2t_i_vec

    # Las componentes normales (escalares) cambian según las fórmulas de colisión 1D
    v1n_f_scalar = (v1n_i_scalar * (m1 - m2) + 2 * m2 * v2n_i_scalar) / (m1 + m2)
    v2n_f_scalar = (v2n_i_scalar * (m2 - m1) + 2 * m1 * v1n_i_scalar) / (m1 + m2)

    # Componentes vectoriales normales finales
    v1n_f_vec = v1n_f_scalar * n_arr
    v2n_f_vec = v2n_f_scalar * n_arr

    # Recomponer las velocidades finales vectoriales
    v1f_arr = v1n_f_vec + v1t_f_vec
    v2f_arr = v2n_f_vec + v2t_f_vec

    return tuple(v1f_arr), tuple(v2f_arr)

@app.route('/simulacion/colision-elastica-3d', methods=['POST'])
def sim_colision_elastica_3d():
    data = request.get_json()
    m1 = data.get('m1_kg')
    v1i = data.get('v1_inicial_mps') # Espera {'x': val, 'y': val, 'z': val}
    m2 = data.get('m2_kg')
    v2i = data.get('v2_inicial_mps') # Espera {'x': val, 'y': val, 'z': val}
    n_vec = data.get('vector_normal_colision') # Espera {'nx': val, 'ny': val, 'nz': val}

    if None in [m1, v1i, m2, v2i, n_vec]:
        return jsonify({"error": "Parámetros 'm1_kg', 'v1_inicial_mps', 'm2_kg', 'v2_inicial_mps', 'vector_normal_colision' son requeridos."}), 400
    if not all(k in v1i for k in ('x','y','z')) or not all(k in v2i for k in ('x','y','z')) or not all(k in n_vec for k in ('nx','ny','nz')):
        return jsonify({"error": "Las velocidades y el vector normal deben tener componentes x, y, z (o nx, ny, nz)."}), 400

    try:
        m1_f = float(m1)
        v1i_tup = (float(v1i['x']), float(v1i['y']), float(v1i['z']))
        m2_f = float(m2)
        v2i_tup = (float(v2i['x']), float(v2i['y']), float(v2i['z']))
        n_vec_tup = (float(n_vec['nx']), float(n_vec['ny']), float(n_vec['nz']))

        if m1_f <= 0 or m2_f <= 0:
            return jsonify({"error": "Las masas deben ser positivas."}), 400
        
        # La función de cálculo se encargará de la normalización del vector normal o de errores relacionados.

        v1f_tup, v2f_tup = calcular_colision_elastica_3d(m1_f, v1i_tup, m2_f, v2i_tup, n_vec_tup)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except TypeError:
         return jsonify({"error": "Formato incorrecto para velocidades o vector normal. Deben ser objetos con x,y,z (o nx,ny,nz)."}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "Conservación del momento lineal (vectorial 3D): m1*v1_i + m2*v2_i = m1*v1_f + m2*v2_f",
        "Conservación de la energía cinética: 0.5*m1*|v1_i|^2 + 0.5*m2*|v2_i|^2 = 0.5*m1*|v1_f|^2 + 0.5*m2*|v2_f|^2",
        "Descomposición de velocidades en: componente normal (escalar) y componente tangencial (vectorial) a la línea de impacto definida por n.",
        "  v_normal_scalar = dot(v, n)",
        "  v_tangencial_vector = v - v_normal_scalar * n",
        "Componentes tangenciales (vectoriales) no cambian: v1t_f_vec = v1t_i_vec, v2t_f_vec = v2t_i_vec",
        "Componentes normales (escalares) se transforman como en colisión 1D:",
        "  v1n_f_scalar = (v1n_i_scalar * (m1 - m2) + 2 * m2 * v2n_i_scalar) / (m1 + m2)",
        "  v2n_f_scalar = (v2n_i_scalar * (m2 - m1) + 2 * m1 * v1n_i_scalar) / (m1 + m2)",
        "Velocidad final: v_f_vector = (v_n_f_scalar * n_vector) + v_t_f_vector"
    ]

    return jsonify({
        "tipo_simulacion": "Colisión Elástica 3D",
        "parametros_entrada": {
            "m1_kg": m1_f,
            "v1_inicial_mps": {"x": v1i_tup[0], "y": v1i_tup[1], "z": v1i_tup[2]},
            "m2_kg": m2_f,
            "v2_inicial_mps": {"x": v2i_tup[0], "y": v2i_tup[1], "z": v2i_tup[2]},
            "vector_normal_colision": {"nx": n_vec_tup[0], "ny": n_vec_tup[1], "nz": n_vec_tup[2]}
        },
        "formulas": formulas,
        "resultados": {
            "v1_final_mps": {"x": v1f_tup[0], "y": v1f_tup[1], "z": v1f_tup[2]},
            "v2_final_mps": {"x": v2f_tup[0], "y": v2f_tup[1], "z": v2f_tup[2]}
        }
    })


def calcular_colision_perfectamente_inelastica_3d(m1, v1ix, v1iy, v1iz, m2, v2ix, v2iy, v2iz):
    """
    Calcula la velocidad final común de dos partículas después de una colisión perfectamente inelástica 3D.
    Retorna (vfx, vfy, vfz)
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")

    # Conservación del momento lineal en cada componente
    px_total_inicial = m1 * v1ix + m2 * v2ix
    py_total_inicial = m1 * v1iy + m2 * v2iy
    pz_total_inicial = m1 * v1iz + m2 * v2iz

    # Masa total después de la colisión
    m_total = m1 + m2

    # Velocidad final común (componentes x, y, z)
    vfx = px_total_inicial / m_total
    vfy = py_total_inicial / m_total
    vfz = pz_total_inicial / m_total

    return vfx, vfy, vfz

@app.route('/simulacion/colision-inelastica-3d', methods=['POST'])
def sim_colision_inelastica_3d():
    data = request.get_json()
    m1 = data.get('m1_kg')
    v1i = data.get('v1_inicial_mps') # Espera {'x': val, 'y': val, 'z': val}
    m2 = data.get('m2_kg')
    v2i = data.get('v2_inicial_mps') # Espera {'x': val, 'y': val, 'z': val}

    if None in [m1, v1i, m2, v2i]:
        return jsonify({"error": "Parámetros 'm1_kg', 'v1_inicial_mps', 'm2_kg', 'v2_inicial_mps' son requeridos."}), 400
    if not all(k in v1i for k in ('x','y','z')) or not all(k in v2i for k in ('x','y','z')):
        return jsonify({"error": "Las velocidades deben tener componentes x, y, z."}), 400

    try:
        m1_f = float(m1)
        v1ix_f, v1iy_f, v1iz_f = float(v1i['x']), float(v1i['y']), float(v1i['z'])
        m2_f = float(m2)
        v2ix_f, v2iy_f, v2iz_f = float(v2i['x']), float(v2i['y']), float(v2i['z'])

        if m1_f <= 0 or m2_f <= 0:
            return jsonify({"error": "Las masas deben ser positivas."}), 400

        vfx, vfy, vfz = calcular_colision_perfectamente_inelastica_3d(m1_f, v1ix_f, v1iy_f, v1iz_f, m2_f, v2ix_f, v2iy_f, v2iz_f)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except TypeError:
         return jsonify({"error": "Formato incorrecto para velocidades. Deben ser objetos con x,y,z."}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "Colisión perfectamente inelástica 3D: los objetos se mueven juntos después del impacto.",
        "Conservación del momento lineal (vectorial 3D): P_inicial = P_final",
        "  m1*v1_i + m2*v2_i = (m1 + m2)*v_f",
        "Componente x: m1*v1ix + m2*v2ix = (m1 + m2)*vfx  => vfx = (m1*v1ix + m2*v2ix) / (m1 + m2)",
        "Componente y: m1*v1iy + m2*v2iy = (m1 + m2)*vfy  => vfy = (m1*v1iy + m2*v2iy) / (m1 + m2)",
        "Componente z: m1*v1iz + m2*v2iz = (m1 + m2)*vfz  => vfz = (m1*v1iz + m2*v2iz) / (m1 + m2)",
        "La energía cinética no se conserva (generalmente se pierde)."
    ]

    return jsonify({
        "tipo_simulacion": "Colisión Perfectamente Inelástica 3D",
        "parametros_entrada": {
            "m1_kg": m1_f,
            "v1_inicial_mps": {"x": v1ix_f, "y": v1iy_f, "z": v1iz_f},
            "m2_kg": m2_f,
            "v2_inicial_mps": {"x": v2ix_f, "y": v2iy_f, "z": v2iz_f}
        },
        "formulas": formulas,
        "resultados": {
            "velocidad_final_comun_mps": {"x": vfx, "y": vfy, "z": vfz}
        }
    })


def calcular_mru(posicion_inicial, velocidad, tiempo_total, num_puntos=100):
    """
    Calcula la posición de un objeto en Movimiento Rectilíneo Uniforme (MRU).
    x(t) = x0 + v*t
    """
    if tiempo_total < 0:
        raise ValueError("El tiempo total no puede ser negativo.")
    if num_puntos <= 1 and tiempo_total > 0:
        # Need at least 2 points to form a line for positive time
        num_puntos = 2 
    elif num_puntos < 1:
        num_puntos = 1 # Single point if time is zero or for safety

    tiempos = np.linspace(0, tiempo_total, num_puntos)
    posiciones = posicion_inicial + velocidad * tiempos
    return list(tiempos), list(posiciones)

@app.route('/simulacion/mru', methods=['POST'])
def sim_mru():
    data = request.get_json()
    posicion_inicial = data.get('posicion_inicial_m', 0.0)
    velocidad = data.get('velocidad_mps')
    tiempo_total = data.get('tiempo_total_s')

    if velocidad is None or tiempo_total is None:
        return jsonify({"error": "Parámetros 'velocidad_mps' y 'tiempo_total_s' son requeridos."}), 400

    try:
        x0 = float(posicion_inicial)
        v = float(velocidad)
        t = float(tiempo_total)

        if t < 0:
            return jsonify({"error": "'tiempo_total_s' no puede ser negativo."}), 400

        tiempos, posiciones = calcular_mru(x0, v, t)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "x(t) = x₀ + v * t  (Posición en función del tiempo)",
        "v = constante (Velocidad constante)",
        "a = 0 (Aceleración nula)"
    ]

    return jsonify({
        "tipo_simulacion": "Movimiento Rectilíneo Uniforme (MRU)",
        "parametros_entrada": {
            "posicion_inicial_m": x0,
            "velocidad_mps": v,
            "tiempo_total_s": t
        },
        "formulas": formulas,
        "resultados": {
            "tiempos_s": tiempos,
            "posiciones_m": posiciones
        }
    })


def calcular_mruv(posicion_inicial, velocidad_inicial, aceleracion, tiempo_total, num_puntos=100):
    """
    Calcula la posición y velocidad de un objeto en Movimiento Rectilíneo Uniformemente Variado (MRUV).
    x(t) = x0 + v0*t + 0.5*a*t^2
    v(t) = v0 + a*t
    """
    if tiempo_total < 0:
        raise ValueError("El tiempo total no puede ser negativo.")
    if num_puntos <= 1 and tiempo_total > 0:
        num_puntos = 2
    elif num_puntos < 1:
        num_puntos = 1

    tiempos = np.linspace(0, tiempo_total, num_puntos)
    posiciones = posicion_inicial + velocidad_inicial * tiempos + 0.5 * aceleracion * tiempos**2
    velocidades = velocidad_inicial + aceleracion * tiempos
    return list(tiempos), list(posiciones), list(velocidades)

@app.route('/simulacion/mruv', methods=['POST'])
def sim_mruv():
    data = request.get_json()
    posicion_inicial = data.get('posicion_inicial_m', 0.0)
    velocidad_inicial = data.get('velocidad_inicial_mps', 0.0)
    aceleracion = data.get('aceleracion_mps2')
    tiempo_total = data.get('tiempo_total_s')

    if aceleracion is None or tiempo_total is None:
        return jsonify({"error": "Parámetros 'aceleracion_mps2' y 'tiempo_total_s' son requeridos."}), 400

    try:
        x0 = float(posicion_inicial)
        v0 = float(velocidad_inicial)
        a = float(aceleracion)
        t = float(tiempo_total)

        if t < 0:
            return jsonify({"error": "'tiempo_total_s' no puede ser negativo."}), 400

        tiempos, posiciones, velocidades = calcular_mruv(x0, v0, a, t)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "x(t) = x₀ + v₀*t + (1/2)*a*t²  (Posición en función del tiempo)",
        "v(t) = v₀ + a*t  (Velocidad en función del tiempo)",
        "a = constante (Aceleración constante)"
    ]

    return jsonify({
        "tipo_simulacion": "Movimiento Rectilíneo Uniformemente Variado (MRUV)",
        "parametros_entrada": {
            "posicion_inicial_m": x0,
            "velocidad_inicial_mps": v0,
            "aceleracion_mps2": a,
            "tiempo_total_s": t
        },
        "formulas": formulas,
        "resultados": {
            "tiempos_s": tiempos,
            "posiciones_m": posiciones,
            "velocidades_mps": velocidades
        }
    })


def calcular_fuerzas_leyes_newton(masa, fuerza_neta, tiempo, velocidad_inicial=0, posicion_inicial=0, num_puntos=100):
    """
    Calcula el movimiento de un objeto bajo una fuerza neta constante (Segunda Ley de Newton).
    F = m*a  => a = F/m
    v(t) = v0 + a*t
    x(t) = x0 + v0*t + 0.5*a*t^2
    """
    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    if num_puntos <= 1 and tiempo > 0:
        num_puntos = 2
    elif num_puntos < 1:
        num_puntos = 1

    aceleracion = fuerza_neta / masa
    tiempos = np.linspace(0, tiempo, num_puntos)
    velocidades = velocidad_inicial + aceleracion * tiempos
    posiciones = posicion_inicial + velocidad_inicial * tiempos + 0.5 * aceleracion * tiempos**2
    
    return list(tiempos), list(posiciones), list(velocidades), aceleracion

@app.route('/simulacion/fuerzas-leyes-newton', methods=['POST'])
def sim_fuerzas_leyes_newton():
    data = request.get_json()
    masa = data.get('masa_kg')
    fuerza_neta = data.get('fuerza_neta_N')
    tiempo = data.get('tiempo_s')
    velocidad_inicial = data.get('velocidad_inicial_mps', 0.0)
    posicion_inicial = data.get('posicion_inicial_m', 0.0)

    if masa is None or fuerza_neta is None or tiempo is None:
        return jsonify({"error": "Parámetros 'masa_kg', 'fuerza_neta_N' y 'tiempo_s' son requeridos."}), 400

    try:
        m = float(masa)
        f_neta = float(fuerza_neta)
        t = float(tiempo)
        v0 = float(velocidad_inicial)
        x0 = float(posicion_inicial)

        if m <= 0:
            return jsonify({"error": "'masa_kg' debe ser positiva."}), 400
        if t < 0:
            return jsonify({"error": "'tiempo_s' no puede ser negativo."}), 400

        tiempos, posiciones, velocidades, aceleracion = calcular_fuerzas_leyes_newton(m, f_neta, t, v0, x0)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "F_neta = m * a (Segunda Ley de Newton)",
        "a = F_neta / m (Aceleración)",
        "v(t) = v₀ + a*t (Velocidad en función del tiempo)",
        "x(t) = x₀ + v₀*t + (1/2)*a*t² (Posición en función del tiempo)"
    ]

    return jsonify({
        "tipo_simulacion": "Fuerzas y Leyes de Newton (2da Ley)",
        "parametros_entrada": {
            "masa_kg": m,
            "fuerza_neta_N": f_neta,
            "tiempo_s": t,
            "velocidad_inicial_mps": v0,
            "posicion_inicial_m": x0
        },
        "formulas": formulas,
        "resultados": {
            "aceleracion_mps2": aceleracion,
            "tiempos_s": tiempos,
            "posiciones_m": posiciones,
            "velocidades_mps": velocidades
        }
    })


def calcular_trabajo_energia_cinetica(masa, fuerza, distancia, velocidad_inicial=0, angulo_fuerza_desplazamiento_grados=0):
    """
    Calcula el trabajo realizado por una fuerza y el cambio en la energía cinética.
    Trabajo (W) = F * d * cos(θ)
    Energía Cinética (K) = 0.5 * m * v^2
    Teorema Trabajo-Energía: W_neto = ΔK = K_final - K_inicial
    """
    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")
    if distancia < 0:
        raise ValueError("La distancia no puede ser negativa.")

    angulo_radianes = np.deg2rad(angulo_fuerza_desplazamiento_grados)
    trabajo = fuerza * distancia * np.cos(angulo_radianes)
    
    energia_cinetica_inicial = 0.5 * masa * velocidad_inicial**2
    # Por el teorema trabajo-energía, W = K_final - K_inicial => K_final = W + K_inicial
    energia_cinetica_final = trabajo + energia_cinetica_inicial

    if energia_cinetica_final < 0:
        # Esto podría pasar si el trabajo es muy negativo (fuerza opuesta al movimiento)
        # y la energía cinética inicial es pequeña. Físicamente, significa que la fuerza
        # detendría el objeto y potencialmente lo movería en dirección opuesta.
        # Para simplificar, asumimos que la velocidad final no puede ser imaginaria.
        # Si K_final es negativo, la velocidad final no es real. 
        # Esto indica que la fuerza detuvo el objeto antes de recorrer toda la 'distancia'.
        # O que la fuerza es tan opuesta que lo frena y lo devuelve.
        # En un modelo simple, podemos decir que la velocidad final es 0 si K_final < 0.
        velocidad_final = 0
        energia_cinetica_final = 0 # El objeto se detiene.
        # Recalcular el trabajo efectivo si se detiene antes.
        # Si v_final = 0, K_final = 0. Entonces W_efectivo = -K_inicial.
        # d_efectiva = -K_inicial / (fuerza * np.cos(angulo_radianes)) si F*cos(theta) != 0
        # Esto se vuelve más complejo, por ahora, si K_final < 0, v_final = 0.
    else:
        velocidad_final = np.sqrt(2 * energia_cinetica_final / masa)
        
    return trabajo, energia_cinetica_inicial, energia_cinetica_final, velocidad_final

@app.route('/simulacion/trabajo-energia', methods=['POST'])
def sim_trabajo_energia():
    data = request.get_json()
    masa = data.get('masa_kg')
    fuerza = data.get('fuerza_N')
    distancia = data.get('distancia_m')
    velocidad_inicial = data.get('velocidad_inicial_mps', 0.0)
    angulo_fuerza_desplazamiento_grados = data.get('angulo_fuerza_desplazamiento_grados', 0.0)

    if masa is None or fuerza is None or distancia is None:
        return jsonify({"error": "Parámetros 'masa_kg', 'fuerza_N' y 'distancia_m' son requeridos."}), 400

    try:
        m = float(masa)
        f = float(fuerza)
        d = float(distancia)
        v0 = float(velocidad_inicial)
        angulo = float(angulo_fuerza_desplazamiento_grados)

        if m <= 0:
            return jsonify({"error": "'masa_kg' debe ser positiva."}), 400
        if d < 0:
             return jsonify({"error": "'distancia_m' no puede ser negativa."}), 400

        trabajo, k_inicial, k_final, v_final = calcular_trabajo_energia_cinetica(m, f, d, v0, angulo)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "W = F * d * cos(θ) (Trabajo realizado por una fuerza constante)",
        "K = (1/2) * m * v² (Energía Cinética)",
        "W_neto = ΔK = K_final - K_inicial (Teorema Trabajo-Energía)"
    ]

    return jsonify({
        "tipo_simulacion": "Trabajo y Energía Cinética",
        "parametros_entrada": {
            "masa_kg": m,
            "fuerza_N": f,
            "distancia_m": d,
            "velocidad_inicial_mps": v0,
            "angulo_fuerza_desplazamiento_grados": angulo
        },
        "formulas": formulas,
        "resultados": {
            "trabajo_realizado_J": trabajo,
            "energia_cinetica_inicial_J": k_inicial,
            "energia_cinetica_final_J": k_final,
            "velocidad_final_mps": v_final
        }
    })


def calcular_energia_potencial_conservacion(masa, altura_inicial, velocidad_inicial_y, num_puntos=100, g=9.81):
    """
    Calcula la energía potencial, cinética y mecánica total de un objeto en caída libre (o subida)
    demostrando la conservación de la energía mecánica.
    U = m*g*h (Energía Potencial Gravitatoria)
    K = 0.5 * m * v^2 (Energía Cinética)
    E_mecanica = U + K = constante (en ausencia de fuerzas no conservativas)
    
    Consideramos solo el movimiento vertical para simplificar la demostración de conservación.
    Si hay velocidad_inicial_x, esta se mantendría constante y solo afectaría K, pero U solo depende de h.
    Para este ejemplo, nos enfocamos en la energía debida al movimiento vertical y la altura.
    """
    if masa <= 0:
        raise ValueError("La masa debe ser positiva.")
    if altura_inicial < 0: # Permitimos altura inicial cero
        pass # Altura inicial puede ser cero
    if num_puntos < 2:
        num_puntos = 2 # Necesitamos al menos dos puntos para mostrar una trayectoria

    # Calcular el tiempo total del vuelo si se lanza hacia arriba y/o cae
    # v_final_y = v_inicial_y - g*t
    # h(t) = h_inicial + v_inicial_y*t - 0.5*g*t^2
    # Tiempo para alcanzar altura máxima (si v_inicial_y > 0): t_max_altura = v_inicial_y / g
    # Altura máxima: h_max = h_inicial + v_inicial_y*t_max_altura - 0.5*g*t_max_altura^2
    # Tiempo para caer desde h_max (o h_inicial si v_inicial_y <=0) hasta h=0:
    # 0 = h_actual - 0.5*g*t_caida^2 => t_caida = sqrt(2*h_actual/g)

    # Determinamos el tiempo total de la simulación para cubrir el movimiento hasta que toque el suelo (h=0)
    # o un tiempo razonable si no se especifica un final claro.
    # Discriminante de la cuadrática para h(t)=0: v_inicial_y^2 - 4*(-0.5*g)*(h_inicial)
    discriminante = velocidad_inicial_y**2 + 2 * g * altura_inicial
    tiempo_hasta_suelo = 0
    if discriminante >= 0:
        # (-v_inicial_y +/- sqrt(discriminante)) / (-g)
        t_sol1 = (velocidad_inicial_y + np.sqrt(discriminante)) / g
        t_sol2 = (velocidad_inicial_y - np.sqrt(discriminante)) / g 
        # Tomamos la solución positiva más grande que represente el tiempo futuro
        if t_sol1 > 0 and t_sol1 >= t_sol2 : tiempo_hasta_suelo = t_sol1
        elif t_sol2 > 0 : tiempo_hasta_suelo = t_sol2
        elif altura_inicial == 0 and velocidad_inicial_y == 0: tiempo_hasta_suelo = 0 # Ya en el suelo y sin velocidad
        else: tiempo_hasta_suelo = 2 # Un tiempo por defecto si no toca el suelo o ya está en él.
    else: # No debería ocurrir si h_inicial >= 0
        tiempo_hasta_suelo = 2 
    
    if tiempo_hasta_suelo == 0 and (altura_inicial > 0 or velocidad_inicial_y != 0): # Si está en el aire, debe haber tiempo de vuelo
        # Si v_inicial_y > 0, tiempo para altura max: v_inicial_y/g. Luego caer desde h_max.
        # Si v_inicial_y <=0, tiempo para caer desde h_inicial.
        # Este es un fallback, la lógica anterior debería cubrirlo.
        if velocidad_inicial_y > 0:
            t_subida = velocidad_inicial_y / g
            h_max_alcanzada = altura_inicial + velocidad_inicial_y * t_subida - 0.5 * g * t_subida**2
            t_caida_desde_max = np.sqrt(2 * h_max_alcanzada / g) if h_max_alcanzada > 0 else 0
            tiempo_hasta_suelo = t_subida + t_caida_desde_max
        else: # Cayendo o lanzado hacia abajo
            tiempo_hasta_suelo = np.sqrt(2 * altura_inicial / g) if altura_inicial > 0 else 0
            if velocidad_inicial_y < 0: # Si lanzado hacia abajo, el tiempo es menor
                 # (-v0y - sqrt(v0y^2 + 2gh0)) / -g = (v0y + sqrt(v0y^2 + 2gh0))/g
                 tiempo_hasta_suelo = (abs(velocidad_inicial_y) + np.sqrt(velocidad_inicial_y**2 + 2*g*altura_inicial))/g

    if tiempo_hasta_suelo <= 1e-6 and (altura_inicial > 0 or abs(velocidad_inicial_y) > 1e-6) : # Evitar división por cero o num_puntos muy denso para t~0
        tiempo_hasta_suelo = 1 # Default time if calculation results in zero but object should move
    elif tiempo_hasta_suelo <= 1e-6 : # Si realmente está en el suelo y sin velocidad, un solo punto de datos.
        num_puntos = 1

    tiempos = np.linspace(0, tiempo_hasta_suelo, num_puntos)
    alturas = altura_inicial + velocidad_inicial_y * tiempos - 0.5 * g * tiempos**2
    # Asegurar que la altura no sea negativa (el objeto se detiene en el suelo)
    alturas = np.maximum(alturas, 0)

    velocidades_y = velocidad_inicial_y - g * tiempos
    # Si la altura es 0, la velocidad y debería ser la de impacto o 0 si ya estaba en el suelo.
    # Si h(t) se hizo 0 antes del final de 'tiempos', v_y debería reflejar eso.
    for i in range(len(tiempos)):
        if i > 0 and alturas[i-1] > 0 and alturas[i] == 0: # Acaba de tocar el suelo
            # Recalcular v_y en el instante antes del impacto si no es el último punto
            # Tiempo de impacto t_impacto tal que h(t_impacto) = 0
            # h_inicial + v_inicial_y*t_impacto - 0.5*g*t_impacto^2 = 0
            # 0.5*g*t_impacto^2 - v_inicial_y*t_impacto - h_inicial = 0
            # t_impacto = (v_inicial_y + sqrt(v_inicial_y^2 + 2*g*h_inicial)) / g (tomando la raíz positiva)
            # Esta es la misma 'tiempo_hasta_suelo' si v_inicial_y es la componente vertical total.
            if tiempo_hasta_suelo > 0:
                 velocidades_y[i] = velocidad_inicial_y - g * tiempo_hasta_suelo # Velocidad de impacto
                 # Y para los puntos posteriores, la velocidad es 0 y altura 0
                 velocidades_y[i+1:] = 0
                 alturas[i+1:] = 0
            break # Salir después de ajustar el impacto
        elif alturas[i] == 0: # Si ya está en el suelo o empieza en el suelo
            velocidades_y[i] = 0 # No hay velocidad vertical si está en el suelo

    energia_potencial = masa * g * alturas
    # Para la energía cinética, si hay una velocidad_x constante, se debe incluir.
    # Aquí asumimos que velocidad_inicial_y es la magnitud total de la velocidad para simplificar
    # o que estamos analizando solo la componente vertical de la energía.
    # Si se quisiera una simulación 2D/3D completa, K usaría |v|^2 = vx^2 + vy^2 + vz^2
    energia_cinetica = 0.5 * masa * velocidades_y**2 
    energia_mecanica_total = energia_potencial + energia_cinetica

    return list(tiempos), list(alturas), list(velocidades_y), list(energia_potencial), list(energia_cinetica), list(energia_mecanica_total)

@app.route('/simulacion/energia-potencial-conservacion', methods=['POST'])
def sim_energia_potencial_conservacion():
    data = request.get_json()
    masa = data.get('masa_kg')
    altura_inicial = data.get('altura_inicial_m')
    velocidad_inicial_y = data.get('velocidad_inicial_y_mps', 0.0) # Velocidad inicial solo en Y para este ejemplo
    g_val = data.get('gravedad_mps2', 9.81)

    if masa is None or altura_inicial is None:
        return jsonify({"error": "Parámetros 'masa_kg' y 'altura_inicial_m' son requeridos."}), 400

    try:
        m = float(masa)
        h0 = float(altura_inicial)
        v0y = float(velocidad_inicial_y)
        g = float(g_val)

        if m <= 0:
            return jsonify({"error": "'masa_kg' debe ser positiva."}), 400
        # h0 puede ser 0
        if g <= 0:
            return jsonify({"error": "'gravedad_mps2' debe ser positiva."}),400

        tiempos, alturas, vels_y, U, K, E_m = calcular_energia_potencial_conservacion(m, h0, v0y, g=g)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "U = m * g * h (Energía Potencial Gravitatoria)",
        "K = (1/2) * m * v² (Energía Cinética, usando v_y para este caso)",
        "E_m = U + K (Energía Mecánica Total)",
        "Conservación de E_m: E_m_inicial = E_m_final (si solo actúan fuerzas conservativas)"
    ]

    return jsonify({
        "tipo_simulacion": "Energía Potencial Gravitatoria y Conservación de Energía Mecánica",
        "parametros_entrada": {
            "masa_kg": m,
            "altura_inicial_m": h0,
            "velocidad_inicial_y_mps": v0y,
            "gravedad_mps2": g
        },
        "formulas": formulas,
        "resultados": {
            "tiempos_s": tiempos,
            "alturas_m": alturas,
            "velocidades_y_mps": vels_y,
            "energia_potencial_J": U,
            "energia_cinetica_J": K,
            "energia_mecanica_total_J": E_m
        }
    })


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

    return list(tiempos), list(posiciones), list(velocidades), list(energia_potencial_elastica), list(energia_cinetica), list(energia_mecanica_total), periodo, frecuencia, omega

@app.route('/simulacion/energia-potencial-elastica', methods=['POST'])
def sim_energia_potencial_elastica():
    data = request.get_json()
    masa = data.get('masa_kg')
    constante_elastica = data.get('constante_elastica_Npm') # N/m
    amplitud = data.get('amplitud_m') # Máximo desplazamiento desde el equilibrio
    tiempo_total = data.get('tiempo_total_s')
    fase_inicial_grados = data.get('fase_inicial_grados', 0.0) # Fase inicial en grados

    if masa is None or constante_elastica is None or amplitud is None or tiempo_total is None:
        return jsonify({"error": "Parámetros 'masa_kg', 'constante_elastica_Npm', 'amplitud_m' y 'tiempo_total_s' son requeridos."}), 400

    try:
        m = float(masa)
        k = float(constante_elastica)
        A = float(amplitud)
        t_total = float(tiempo_total)
        phi_grados = float(fase_inicial_grados)
        phi_rad = np.deg2rad(phi_grados)

        if m <= 0: return jsonify({"error": "'masa_kg' debe ser positiva."}), 400
        if k <= 0: return jsonify({"error": "'constante_elastica_Npm' debe ser positiva."}), 400
        if A < 0: return jsonify({"error": "'amplitud_m' no puede ser negativa."}), 400
        if t_total < 0: return jsonify({"error": "'tiempo_total_s' no puede ser negativo."}), 400

        tiempos, x, v, U_e, K, E_m, T, f, omega = calcular_energia_potencial_elastica(m, k, A, t_total, fase_inicial_rad=phi_rad)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error en el cálculo: " + str(e)}), 500

    formulas = [
        "ω = sqrt(k/m) (Frecuencia Angular)",
        "T = 2π/ω (Período)",
        "f = 1/T (Frecuencia)",
        "x(t) = A * cos(ω*t + φ) (Posición)",
        "v(t) = -A * ω * sin(ω*t + φ) (Velocidad)",
        "U_elástica = (1/2) * k * x² (Energía Potencial Elástica)",
        "K = (1/2) * m * v² (Energía Cinética)",
        "E_mecánica = U_elástica + K (Energía Mecánica Total, conservada)"
    ]

    return jsonify({
        "tipo_simulacion": "Energía Potencial Elástica y Conservación (Sistema Masa-Resorte)",
        "parametros_entrada": {
            "masa_kg": m,
            "constante_elastica_Npm": k,
            "amplitud_m": A,
            "tiempo_total_s": t_total,
            "fase_inicial_grados": phi_grados
        },
        "formulas": formulas,
        "resultados": {
            "frecuencia_angular_radps": omega,
            "periodo_s": T,
            "frecuencia_Hz": f,
            "tiempos_s": tiempos,
            "posiciones_m": x,
            "velocidades_mps": v,
            "energia_potencial_elastica_J": U_e,
            "energia_cinetica_J": K,
            "energia_mecanica_total_J": E_m
        }
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001) # Cambiado el puerto para evitar conflictos comunes