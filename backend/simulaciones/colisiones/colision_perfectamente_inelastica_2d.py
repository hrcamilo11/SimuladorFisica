from backend.Ecuaciones.colisiones.colision_perfectamente_inelastica_2d import calcular_colision_perfectamente_inelastica_2d

def simular_colision_perfectamente_inelastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy):
    """
    Función para simular una colisión perfectamente inelástica 2D, diseñada como un endpoint de API.
    """
    try:
        vfx, vfy, estados_simulacion = calcular_colision_perfectamente_inelastica_2d(m1, v1ix, v1iy, m2, v2ix, v2iy)
        
        return {
            "success": True,
            "message": "Cálculo de colisión perfectamente inelástica 2D exitoso.",
            "parametros_entrada": {
                "m1": m1,
                "v1ix": v1ix,
                "v1iy": v1iy,
                "m2": m2,
                "v2ix": v2ix,
                "v2iy": v2iy
            },
            "resultados": {
                "vfx_final": vfx,
                "vfy_final": vfy
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
                "v2iy": v2iy
            },
            "resultados": None,
            "estados_simulacion": []
        }