from backend.Ecuaciones.colisiones.colision_elastica_2d import calcular_colision_elastica_2d

def simular_colision_elastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy, nx, ny):
    """
    Función para simular una colisión elástica 2D, diseñada como un endpoint de API.
    """
    try:
        v1fx_f, v1fy_f, v2fx_f, v2fy_f, estados_simulacion = calcular_colision_elastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy, nx, ny)
        
        return {
            "success": True,
            "message": "Cálculo de colisión elástica 2D exitoso.",
            "parametros_entrada": {
                "m1": m1,
                "v1ix": v1ix,
                "v1iy": v1iy,
                "m2": m2,
                "v2ix": v2ix,
                "v2iy": v2iy,
                "nx": nx,
                "ny": ny
            },
            "resultados": {
                "v1fx_final": v1fx_f,
                "v1fy_final": v1fy_f,
                "v2fx_final": v2fx_f,
                "v2fy_final": v2fy_f
            },
            "estados_simulacion": estados_simulacion
        }
    except ValueError as e:
        return {
            "success": False,
            "message": str(e),
            "parametros_entrada": {
                "m1": m1,
                "v1ix": v1ix,
                "v1iy": v1iy,
                "m2": m2,
                "v2ix": v2ix,
                "v2iy": v2iy,
                "nx": nx,
                "ny": ny
            },
            "resultados": None,
            "estados_simulacion": []
        }
