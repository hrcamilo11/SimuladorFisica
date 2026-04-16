import { NextResponse } from 'next/server';
import { simularLeyOhm, simularResistencia, simularCircuitoSerie, simularCircuitoParalelo, simularPotenciaElectrica, simularCapacitancia, simularInductancia, simularMagnetismo, simularLeyesKirchhoff } from '@/lib/physics/electricidad';

export async function POST(req: Request, { params }: { params: Promise<{ simulacion: string }> }) {
  try {
    const data = await req.json();
    const { simulacion } = await params;
    let result;

    switch (simulacion) {
      case 'ley-ohm':
        result = simularLeyOhm(data.voltaje, data.corriente, data.resistencia);
        break;
      case 'resistencia':
        result = simularResistencia(data.resistividad !== undefined ? data.resistividad : 1.68e-8, data.longitud || 1, data.area || 1e-6);
        break;
      case 'calculos-circuitos':
        if (data.tipo_circuito === 'paralelo') {
            result = simularCircuitoParalelo(data.resistencias || [10, 10], data.voltaje_total || 12);
        } else {
            result = simularCircuitoSerie(data.resistencias || [10, 10], data.voltaje_total || 12);
        }
        break;
      case 'potencia-electrica':
        result = simularPotenciaElectrica(data.voltaje, data.corriente, data.resistencia);
        break;
      case 'capacitancia':
        result = simularCapacitancia(data.carga, data.voltaje, data.capacitancia);
        break;
      case 'inductancia':
        result = simularInductancia(data.flujo_magnetico || 0.01, data.corriente || 1, data.numero_espiras || 100);
        break;
      case 'magnetismo':
        result = simularMagnetismo(data.tipo_calculo || 'campo_magnetico', data);
        break;
      case 'leyes-kirchhoff':
        result = simularLeyesKirchhoff(data.tipo_ley || 'voltaje', data);
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
