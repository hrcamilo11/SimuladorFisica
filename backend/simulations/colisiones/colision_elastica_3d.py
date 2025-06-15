from backend.Ecuaciones.colisiones.colision_elastica_3d import calcular_colision_elastica_3d

def simular_colision_elastica_3d(m1, v1i, m2, v2i, n_vec):
    """
    Función para simular una colisión elástica 3D, diseñada como un endpoint de API.
    """
    try:
        v1f, v2f, estados_simulacion = calcular_colision_elastica_3d(m1, v1i, m2, v2i, n_vec)
        
        return {
            "success": True,
            "message": "Cálculo de colisión elástica 3D exitoso.",
            "parametros_entrada": {
                "m1": m1,
                "v1i": v1i,
                "m2": m2,
                "v2i": v2i,
                "n_vec": n_vec
            },
            "resultados": {
                "v1_final": v1f,
                "v2_final": v2f
            },
            "estados_simulacion": estados_simulacion
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "parametros_entrada": {
                "m1": m1,
                "v1i": v1i,
                "m2": m2,
                "v2i": v2i,
                "n_vec": n_vec
            },
            "resultados": None,
            "estados_simulacion": []
        }
