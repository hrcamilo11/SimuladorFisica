import { NextResponse } from 'next/server';
import { simularLeyesNewton, simularPlanoInclinado, simularPlanoInclinadoPolea } from '@/lib/physics/dinamica';

export async function POST(req: Request, { params }: { params: Promise<{ simulacion: string }> }) {
  try {
    const data = await req.json();
    const { simulacion } = await params;
    let result;

    switch (simulacion) {
      case 'leyes-newton':
        result = simularLeyesNewton(data.masa, data.fuerza_aplicada, data.coeficiente_rozamiento, data.tiempo_total_simulacion, data.num_puntos);
        break;
      case 'plano-inclinado':
        result = simularPlanoInclinado(data.masa, data.angulo_inclinacion, data.coeficiente_rozamiento_cinetico, data.distancia_recorrida, data.velocidad_inicial, data.tiempo_total_simulacion, data.num_puntos);
        break;
      case 'plano-inclinado-polea':
        result = simularPlanoInclinadoPolea(data.masa1, data.masa2, data.angulo_inclinacion_grados, data.coeficiente_rozamiento_estatico, data.coeficiente_rozamiento_cinetico);
        break;
      default:
        return NextResponse.json({ success: false, message: `Simulación no encontrada: ${simulacion}` }, { status: 404 });
    }
    return NextResponse.json({ success: true, ...result });
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : 'Error durante la simulación';
    return NextResponse.json({ success: false, message: msg }, { status: 400 });
  }
}
