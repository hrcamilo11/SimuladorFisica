import { NextResponse } from 'next/server';
import {
  simularCaidaLibre,
  simularMRU,
  simularMRUV,
  simularTiroParabolico,
  simularMCU,
  simularMAS,
  simularPenduloSimple
} from '@/lib/physics/cinematica';

export async function POST(
  req: Request,
  { params }: { params: Promise<{ simulacion: string }> }
) {
  try {
    const data = await req.json();
    const { simulacion } = await params;
    
    let result;

    switch (simulacion) {
      case 'caida-libre':
        result = simularCaidaLibre(
          data.altura_inicial,
          data.tiempo_total_simulacion,
          data.num_puntos || 100
        );
        break;
      case 'mru':
        result = simularMRU(
          data.posicion_inicial,
          data.velocidad,
          data.tiempo_total_simulacion,
          data.num_puntos || 100
        );
        break;
      case 'mruv':
        result = simularMRUV(
          data.posicion_inicial,
          data.velocidad_inicial,
          data.aceleracion,
          data.tiempo_total_simulacion,
          data.num_puntos || 100
        );
        break;
      case 'tiro-parabolico':
        result = simularTiroParabolico(
          data.velocidad_inicial,
          data.angulo_lanzamiento || data.angulo_grados,
          data.altura_inicial || 0,
          data.tiempo_total_simulacion,
          data.num_puntos || 100
        );
        break;
      case 'movimiento-circular-uniforme':
        result = simularMCU(
          data.radio,
          data.velocidad_angular,
          data.tiempo_total_simulacion,
          data.posicion_angular_inicial || 0,
          data.num_puntos || 100
        );
        break;
      case 'movimiento-armonico-simple':
        result = simularMAS(
          data.amplitud,
          data.frecuencia_angular,
          data.fase_inicial || 0,
          data.tiempo_total_simulacion,
          data.num_puntos || 100
        );
        break;
      case 'pendulo-simple':
        result = simularPenduloSimple(
          data.longitud,
          data.angulo_inicial,
          data.velocidad_angular_inicial || 0,
          data.tiempo_total_simulacion,
          data.num_puntos || 100
        );
        break;
      default:
        return NextResponse.json({ success: false, message: `Simulación no encontrada: ${simulacion}` }, { status: 404 });
    }

    return NextResponse.json({
      success: true,
      ...result
    });

  } catch (error: unknown) {
    const errorMsg = error instanceof Error ? error.message : 'Error occurred during simulation';
    return NextResponse.json({
      success: false,
      message: errorMsg
    }, { status: 400 });
  }
}
