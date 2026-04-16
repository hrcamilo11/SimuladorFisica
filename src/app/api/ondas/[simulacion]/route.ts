import { NextResponse } from 'next/server';
import { simularOndas } from '@/lib/physics/ondas';

export async function POST(req: Request, { params }: { params: Promise<{ simulacion: string }> }) {
  try {
    const data = await req.json();
    const { simulacion } = await params;
    let result;

    switch (simulacion) {
      case 'ondas':
        result = simularOndas(data.tipo_calculo || 'velocidad_onda', data);
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
