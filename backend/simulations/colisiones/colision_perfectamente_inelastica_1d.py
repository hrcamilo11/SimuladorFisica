from backend.Ecuaciones.colisiones.colision_perfectamente_inelastica_1d import calcular_colision_perfectamente_inelastica_1d

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