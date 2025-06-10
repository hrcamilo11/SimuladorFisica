import numpy as np

def calcular_colision_perfectamente_inelastica_1d(m1, v1_inicial, m2, v2_inicial):
    """
    Calcula la velocidad final común de dos objetos después de una colisión perfectamente inelástica 1D.
    Los objetos quedan unidos después del choque.
    m1, m2: masas de los objetos.
    v1_inicial, v2_inicial: velocidades iniciales de los objetos.
    Retorna v_final_comun, estados_simulacion.
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Las masas deben ser positivas.")

    # Conservación del momento lineal: m1*v1_i + m2*v2_i = (m1 + m2)*v_f_comun
    v_final_comun = (m1 * v1_inicial + m2 * v2_inicial) / (m1 + m2)
    
    # Para colisiones, el concepto de "tiempo de simulación" es instantáneo.
    # Creamos una matriz de estados para la animación.
    # Representaremos el estado inicial y el estado final.
    # Cada fila: [tiempo, posicion_x_obj1, posicion_y_obj1, velocidad_x_obj1, velocidad_y_obj1, posicion_x_obj2, posicion_y_obj2, velocidad_x_obj2, velocidad_y_obj2]
    # En 1D, y-componentes y posiciones son 0 o irrelevantes para el cálculo, pero se incluyen para consistencia con 2D/3D.
    # Asumimos que la colisión ocurre en x=0 para simplificar la visualización.
    estados_simulacion = [
        [0, -1.0, 0, v1_inicial, 0, 1.0, 0, v2_inicial, 0], # Estado inicial (posiciones arbitrarias para visualización)
        [0, 0.0, 0, v_final_comun, 0, 0.0, 0, v_final_comun, 0]    # Estado final (mismo tiempo, nuevas velocidades, objetos unidos en el origen)
    ]

    return v_final_comun, estados_simulacion

def simular_colision_perfectamente_inelastica_1d(m1, v1_inicial, m2, v2_inicial):
    """
    Función para simular una colisión perfectamente inelástica 1D, diseñada como un endpoint de API.
    """
    try:
        v_final_comun, estados_simulacion = calcular_colision_perfectamente_inelastica_1d(m1, v1_inicial, m2, v2_inicial)
        
        return {
            "success": True,
            "message": "Cálculo de colisión perfectamente inelástica 1D exitoso.",
            "parametros_entrada": {
                "m1": m1,
                "v1_inicial": v1_inicial,
                "m2": m2,
                "v2_inicial": v2_inicial
            },
            "resultados": {
                "v_final_comun": v_final_comun
            },
            "estados_simulacion": estados_simulacion
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "parametros_entrada": {
                "m1": m1,
                "v1_inicial": v1_inicial,
                "m2": m2,
                "v2_inicial": v2_inicial
            },
            "resultados": None,
            "estados_simulacion": []
        }