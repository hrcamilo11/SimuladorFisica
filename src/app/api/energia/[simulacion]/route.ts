import { NextResponse } from 'next/server';
import { simularTrabajoEnergia, simularEnergiaPotencialGravitatoria, simularEnergiaPotencialElastica } from '@/lib/physics/energia';

export async function POST(req: Request, { params }: { params: Promise<{ simulacion: string }> }) {
  try {
    const data = await req.json();
    const { simulacion } = await params;
    let result;

    switch (simulacion) {
      case 'trabajo-energia':
        result = simularTrabajoEnergia(data.masa, data.velocidad_inicial, data.velocidad_final);
        break;
      case 'energia-potencial-gravitatoria':
        result = simularEnergiaPotencialGravitatoria(data.masa, data.altura);
        break;
      case 'energia-potencial-elastica':
        result = simularEnergiaPotencialElastica(data.constante_elastica, data.deformacion);
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
