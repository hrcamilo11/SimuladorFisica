import { NextResponse } from 'next/server';
import { simularColisionElastica1D, simularColisionElastica2D, simularColisionElastica3D, simularColisionInelastica1D, simularColisionInelastica2D } from '@/lib/physics/colisiones';

export async function POST(req: Request, { params }: { params: Promise<{ simulacion: string }> }) {
  try {
    const data = await req.json();
    const { simulacion } = await params;
    let result;

    switch (simulacion) {
      case 'colision-elastica-1d':
        result = simularColisionElastica1D(data.masa1, data.velocidad_inicial1, data.masa2, data.velocidad_inicial2);
        break;
      case 'colision-elastica-2d':
        result = simularColisionElastica2D(data.masa1, data.velocidad_inicial1, data.angulo_inicial1_grados, data.masa2, data.velocidad_inicial2, data.angulo_inicial2_grados);
        break;
      case 'colision-elastica-3d':
        result = simularColisionElastica3D(data.masa1, data.v1x, data.v1y, data.v1z, data.masa2, data.v2x, data.v2y, data.v2z);
        break;
      case 'colision-perfectamente-inelastica-1d':
        result = simularColisionInelastica1D(data.masa1, data.velocidad_inicial1, data.masa2, data.velocidad_inicial2);
        break;
      case 'colision-perfectamente-inelastica-2d':
        result = simularColisionInelastica2D(data.masa1, data.v1x, data.v1y, data.masa2, data.v2x, data.v2y);
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
