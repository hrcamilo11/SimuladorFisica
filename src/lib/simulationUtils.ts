import { SimulationResult, ChartDataPoint, ParamDefinition, Formula } from '@/types/simulation';

export const getFormulasForSimulation = (simSlug: string): Formula[] => {
  switch (simSlug) {
    case 'caida-libre':
      return [
        { formula: 'y = y₀ + v₀t - ½gt²', description: 'Posición en caída libre' },
        { formula: 'v = v₀ - gt', description: 'Velocidad en caída libre' }
      ];
    case 'mru':
      return [
        { formula: 'x = x₀ + vt', description: 'Posición en MRU' }
      ];
    case 'mruv':
      return [
        { formula: 'x = x₀ + v₀t + ½at²', description: 'Posición en MRUV' },
        { formula: 'v = v₀ + at', description: 'Velocidad en MRUV' }
      ];
    case 'tiro-parabolico':
      return [
        { formula: 'x = x₀ + v₀ₓt', description: 'Posición horizontal en tiro parabólico' },
        { formula: 'y = y₀ + v₀ᵧt - ½gt²', description: 'Posición vertical en tiro parabólico' }
      ];
    case 'movimiento-circular-uniforme':
      return [
        { formula: 'θ = ωt', description: 'Ángulo en MCU' },
        { formula: 'v = ωr', description: 'Velocidad tangencial en MCU' },
        { formula: 'a_c = v²/r = ω²r', description: 'Aceleración centrípeta en MCU' }
      ];
    case 'movimiento-armonico-simple':
      return [
        { formula: 'x(t) = A cos(ωt + φ)', description: 'Posición en MAS' },
        { formula: 'v(t) = -Aω sen(ωt + φ)', description: 'Velocidad en MAS' },
        { formula: 'a(t) = -Aω² cos(ωt + φ)', description: 'Aceleración en MAS' }
      ];
    case 'pendulo-simple':
      return [
        { formula: 'T = 2π√(L/g)', description: 'Período del péndulo simple' }
      ];
    case 'plano-inclinado':
    case 'plano-inclinado-polea':
      return [
        { formula: 'F_n = mg cos(θ)', description: 'Fuerza normal en plano inclinado' },
        { formula: 'F_g_x = mg sen(θ)', description: 'Componente de la gravedad paralela al plano' }
      ];
    case 'leyes-newton':
    case 'fuerzas-leyes-newton':
      return [
        { formula: 'F = ma', description: 'Segunda Ley de Newton' }
      ];
    case 'energia-potencial-conservacion':
      return [
        { formula: 'E_total = E_c + E_p = constante', description: 'Conservación de la energía mecánica' },
        { formula: 'E_c = ½mv²', description: 'Energía cinética' },
        { formula: 'E_p = mgh', description: 'Energía potencial gravitatoria' }
      ];
    case 'energia-potencial-elastica':
      return [
        { formula: 'E_p_elastica = ½kx²', description: 'Energía potencial elástica' }
      ];
    case 'energia-potencial-gravitatoria':
      return [
        { formula: 'E_p = mgh', description: 'Energía potencial gravitatoria' }
      ];
    case 'trabajo-energia':
      return [
        { formula: 'W = ΔE_c = ½mv_f² - ½mv_i²', description: 'Teorema de trabajo y energía' }
      ];
    case 'colision-elastica-1d':
    case 'colision-elastica-2d':
    case 'colision-elastica-3d':
      return [
        { formula: 'm₁v₁ᵢ + m₂v₂ᵢ = m₁v₁_f + m₂v₂_f', description: 'Conservación del momentum' },
        { formula: '½m₁v₁ᵢ² + ½m₂v₂ᵢ² = ½m₁v₁_f² + ½m₂v₂_f²', description: 'Conservación de la energía cinética' }
      ];
    case 'colision-perfectamente-inelastica-1d':
    case 'colision-perfectamente-inelastica-2d':
      return [
        { formula: 'm₁v₁ᵢ + m₂v₂ᵢ = (m₁ + m₂)v_f', description: 'Conservación del momentum (Inelástica)' }
      ];
    case 'ley-ohm':
      return [{ formula: 'V = I × R', description: 'Ley de Ohm' }];
    case 'resistencia':
      return [{ formula: 'R = ρ(L/A)', description: 'Resistencia eléctrica de un conductor' }];
    case 'potencia-electrica':
      return [{ formula: 'P = V × I = I²R = V²/R', description: 'Potencia Eléctrica' }];
    case 'calculos-circuitos':
      return [
        { formula: 'R_eq_serie = R₁ + R₂ + ...', description: 'Resistencia Equivalente en Serie' },
        { formula: '1/R_eq_paralelo = 1/R₁ + 1/R₂ + ...', description: 'Resistencia Equivalente en Paralelo' }
      ];
    case 'capacitancia':
      return [{ formula: 'C = Q / V', description: 'Capacitancia' }];
    case 'inductancia':
      return [{ formula: 'L = (N × Φ) / I', description: 'Inductancia' }];
    case 'leyes-kirchhoff':
      return [
        { formula: 'Σ I_entra = Σ I_sale', description: 'Ley de Nodos (Corriente)' },
        { formula: 'Σ V = 0', description: 'Ley de Mallas (Voltaje)' }
      ];
    case 'magnetismo':
      return [{ formula: 'B = (μ₀I)/(2πr)', description: 'Campo Magnético' }];
    case 'ondas':
      return [
        { formula: 'v = f × λ', description: 'Velocidad de la onda' },
        { formula: 'f = 1 / T', description: 'Frecuencia y Período' }
      ];
    default:
      return [];
  }
};

export const isChartableSimulation = (simSlug: string): boolean => {
  const chartableSimulations = [
    'caida-libre',
    'tiro-parabolico',
    'plano-inclinado',
    'movimiento-circular-uniforme',
    'movimiento-armonico-simple',
    'pendulo-simple',
    'mru',
    'mruv',
    'leyes-newton',
    'fuerzas-leyes-newton',
    'energia-potencial-conservacion',
    'energia-potencial-elastica',
  ];
  return chartableSimulations.includes(simSlug);
};

export const formatDataForChart = (simulationData: { resultados: SimulationResult }, simSlug: string): ChartDataPoint[] => {
  const resultados = simulationData.resultados;
  if (resultados.estados_simulacion && Array.isArray(resultados.estados_simulacion) && resultados.estados_simulacion.length > 0) {
    return resultados.estados_simulacion.map((estado: Record<string, unknown>) => {
      const chartPoint: ChartDataPoint = { tiempo: estado.tiempo as number };
      for (const key in estado) {
        if (key !== 'tiempo' && typeof estado[key] === 'number') {
          chartPoint[key] = estado[key] as number;
        }
      }
      return chartPoint;
    });
  } else {
    // Legacy fallback format or formats not containing estados_simulacion
    const tiempos = resultados.tiempos || [];
    const posiciones = resultados.posiciones || [];
    const velocidades = resultados.velocidades || [];
    const aceleraciones = resultados.aceleraciones || [];
    let data: ChartDataPoint[] = [];

    switch (simSlug) {
      case 'caida-libre':
        data = tiempos.map((t, i) => ({ tiempo: t, posicion: posiciones[i] || 0, velocidad: velocidades[i] || 0, aceleracion: aceleraciones[i] || 0 }));
        break;
      case 'tiro-parabolico':
        data = tiempos.map((t, i) => ({ tiempo: t, posicion_x: resultados.posiciones_x?.[i] || 0, posicion_y: resultados.posiciones_y?.[i] || 0, velocidad_x: resultados.velocidades_x?.[i] || 0, velocidad_y: resultados.velocidades_y?.[i] || 0, aceleracion_x: resultados.aceleraciones_x?.[i] || 0, aceleracion_y: resultados.aceleraciones_y?.[i] || 0 }));
        break;
      case 'plano-inclinado':
        data = tiempos.map((t, i) => ({ tiempo: t, posicion_x: resultados.posiciones_x?.[i] || 0, posicion_y: resultados.posiciones_y?.[i] || 0, velocidad_x: resultados.velocidades_x?.[i] || 0, velocidad_y: resultados.velocidades_y?.[i] || 0, aceleracion_x: resultados.aceleraciones_x?.[i] || 0, aceleracion_y: resultados.aceleraciones_y?.[i] || 0, fuerza: resultados.fuerzas?.[i] || 0 }));
        break;
      case 'movimiento-circular-uniforme':
        data = tiempos.map((t, i) => ({ tiempo: t, posicion_x: resultados.posiciones_x?.[i] || 0, posicion_y: resultados.posiciones_y?.[i] || 0, angulo: resultados.angulos?.[i] || 0 }));
        break;
      case 'movimiento-armonico-simple':
        data = tiempos.map((t, i) => ({ tiempo: t, posicion_x: resultados.posiciones?.[i] || 0, velocidad_x: resultados.velocidades?.[i] || 0, aceleracion_x: resultados.aceleraciones?.[i] || 0 }));
        break;
      case 'pendulo-simple':
        data = tiempos.map((t, i) => ({ tiempo: t, posicion_angular: resultados.posiciones_angular?.[i] || 0, velocidad_angular: resultados.velocidades_angular?.[i] || 0, aceleracion_angular: resultados.aceleraciones_angular?.[i] || 0, posicion_x_cartesiana: resultados.posiciones_x_cartesianas?.[i] || 0, posicion_y_cartesiana: resultados.posiciones_y_cartesianas?.[i] || 0 }));
        break;
      case 'mru':
        data = tiempos.map((t, i) => ({ tiempo: t, posicion: posiciones[i] || 0, velocidad: velocidades[i] || 0 }));
        break;
      case 'mruv':
        data = tiempos.map((t, i) => ({ tiempo: t, posicion: posiciones[i] || 0, velocidad: velocidades[i] || 0, aceleracion: aceleraciones[i] || 0 }));
        break;
      case 'leyes-newton':
      case 'fuerzas-leyes-newton':
        data = tiempos.map((t, i) => ({ tiempo: t, fuerza: resultados.fuerzas?.[i] || 0, aceleracion: resultados.aceleraciones?.[i] || 0 }));
        break;
      case 'energia-potencial-conservacion':
        data = tiempos.map((t, i) => ({ tiempo: t, energia_cinetica: resultados.energias_cineticas?.[i] || 0, energia_potencial: resultados.energias_potenciales?.[i] || 0, energia_total: resultados.energias_totales?.[i] || 0 }));
        break;
      case 'energia-potencial-elastica':
        data = tiempos.map((t, i) => ({ tiempo: t, energia_potencial_elastica: resultados.energias_potenciales_elasticas?.[i] || 0, posicion: resultados.posiciones?.[i] || 0 }));
        break;
      default:
        data = tiempos.map((t, i) => ({ tiempo: t, posicion: posiciones[i] || 0 }));
        break;
    }
    return data;
  }
};

export const getExpectedParamsForSimulation = (simSlug: string): ParamDefinition[] => {
  switch (simSlug) {
    // Cinemática
    case 'caida-libre':
      return [
        { name: 'altura_inicial', label: 'Altura Inicial', unit: 'm', defaultValue: 100 },
        { name: 'tiempo_total_simulacion', label: 'Tiempo de Simulación', unit: 's', defaultValue: 5 },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '', defaultValue: 100 },
      ];
    case 'mru':
      return [
        { name: 'posicion_inicial', label: 'Posición Inicial', unit: 'm', defaultValue: 0 },
        { name: 'velocidad', label: 'Velocidad', unit: 'm/s', defaultValue: 10 },
        { name: 'tiempo_total_simulacion', label: 'Tiempo', unit: 's', defaultValue: 5 },
        { name: 'num_puntos', label: 'Puntos', unit: '', defaultValue: 100 },
      ];
    case 'mruv':
      return [
        { name: 'posicion_inicial', label: 'Posición Inicial', unit: 'm', defaultValue: 0 },
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s', defaultValue: 0 },
        { name: 'aceleracion', label: 'Aceleración', unit: 'm/s²', defaultValue: 9.8 },
        { name: 'tiempo_total_simulacion', label: 'Tiempo', unit: 's', defaultValue: 5 },
        { name: 'num_puntos', label: 'Puntos', unit: '', defaultValue: 100 },
      ];
    case 'tiro-parabolico':
      return [
        { name: 'altura_inicial', label: 'Altura Inicial', unit: 'm', defaultValue: 0 },
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s', defaultValue: 30 },
        { name: 'angulo_lanzamiento', label: 'Ángulo', unit: 'grados', defaultValue: 45 },
        { name: 'num_puntos', label: 'Puntos', unit: '', defaultValue: 100 },
      ];
    case 'movimiento-circular-uniforme':
      return [
        { name: 'radio', label: 'Radio', unit: 'm', defaultValue: 5 },
        { name: 'velocidad_angular', label: 'Velocidad Angular', unit: 'rad/s', defaultValue: 2 },
        { name: 'tiempo_total_simulacion', label: 'Tiempo', unit: 's', defaultValue: 5 },
        { name: 'num_puntos', label: 'Puntos', unit: '', defaultValue: 100 },
      ];
    case 'movimiento-armonico-simple':
      return [
        { name: 'amplitud', label: 'Amplitud', unit: 'm', defaultValue: 2 },
        { name: 'frecuencia_angular', label: 'Frecuencia Angular', unit: 'rad/s', defaultValue: 3.14 },
        { name: 'fase_inicial', label: 'Fase Inicial', unit: 'rad', defaultValue: 0 },
        { name: 'tiempo_total_simulacion', label: 'Tiempo', unit: 's', defaultValue: 5 },
        { name: 'num_puntos', label: 'Puntos', unit: '', defaultValue: 100 },
      ];
    case 'pendulo-simple':
      return [
        { name: 'longitud', label: 'Longitud del Hilo', unit: 'm', defaultValue: 2 },
        { name: 'angulo_inicial', label: 'Ángulo Inicial', unit: 'grados', defaultValue: 30 },
        { name: 'tiempo_total_simulacion', label: 'Tiempo', unit: 's', defaultValue: 5 },
        { name: 'num_puntos', label: 'Puntos', unit: '', defaultValue: 100 },
      ];

    // Dinámica
    case 'leyes-newton':
    case 'fuerzas-leyes-newton':
      return [
        { name: 'masa', label: 'Masa', unit: 'kg', defaultValue: 10 },
        { name: 'fuerza_aplicada', label: 'Fuerza Aplicada', unit: 'N', defaultValue: 50 },
        { name: 'coeficiente_rozamiento', label: 'Coeficiente Rozamiento', unit: '', defaultValue: 0.1 },
        { name: 'tiempo_total_simulacion', label: 'Tiempo', unit: 's', defaultValue: 5 },
        { name: 'num_puntos', label: 'Puntos', unit: '', defaultValue: 100 },
      ];
    case 'plano-inclinado':
      return [
        { name: 'masa', label: 'Masa', unit: 'kg', defaultValue: 5 },
        { name: 'angulo_inclinacion', label: 'Ángulo', unit: 'grados', defaultValue: 30 },
        { name: 'coeficiente_rozamiento_cinetico', label: 'Coeficiente Rozamiento', unit: '', defaultValue: 0.1 },
        { name: 'distancia_recorrida', label: 'Distancia', unit: 'm', defaultValue: 20 },
        { name: 'velocidad_inicial', label: 'Velocidad inicial', unit: 'm/s', defaultValue: 0 },
      ];
    case 'plano-inclinado-polea':
      return [
        { name: 'masa1', label: 'Masa en plano', unit: 'kg', defaultValue: 5 },
        { name: 'masa2', label: 'Masa colgada', unit: 'kg', defaultValue: 10 },
        { name: 'angulo_inclinacion_grados', label: 'Ángulo del plano', unit: 'grados', defaultValue: 30 },
        { name: 'coeficiente_rozamiento_estatico', label: 'Mu elástico', unit: '', defaultValue: 0.2 },
        { name: 'coeficiente_rozamiento_cinetico', label: 'Mu cinético', unit: '', defaultValue: 0.1 },
      ];

    // Energía
    case 'energia-potencial-conservacion':
    case 'energia-potencial-gravitatoria':
      return [
        { name: 'masa', label: 'Masa', unit: 'kg', defaultValue: 10 },
        { name: 'altura', label: 'Altura', unit: 'm', defaultValue: 20 },
      ];
    case 'energia-potencial-elastica':
      return [
        { name: 'constante_elastica', label: 'Constante Elástica (k)', unit: 'N/m', defaultValue: 500 },
        { name: 'deformacion', label: 'Deformación (x)', unit: 'm', defaultValue: 0.5 },
      ];
    case 'trabajo-energia':
      return [
        { name: 'masa', label: 'Masa', unit: 'kg', defaultValue: 10 },
        { name: 'velocidad_inicial', label: 'Velocidad inicial', unit: 'm/s', defaultValue: 0 },
        { name: 'velocidad_final', label: 'Velocidad final', unit: 'm/s', defaultValue: 20 },
      ];

    // Colisiones
    case 'colision-elastica-1d':
    case 'colision-perfectamente-inelastica-1d':
      return [
        { name: 'masa1', label: 'Masa 1', unit: 'kg', defaultValue: 5 },
        { name: 'velocidad_inicial1', label: 'Velocidad Inicial 1', unit: 'm/s', defaultValue: 10 },
        { name: 'masa2', label: 'Masa 2', unit: 'kg', defaultValue: 5 },
        { name: 'velocidad_inicial2', label: 'Velocidad Inicial 2', unit: 'm/s', defaultValue: -5 },
      ];
    case 'colision-elastica-2d':
      return [
        { name: 'masa1', label: 'Masa 1', unit: 'kg', defaultValue: 5 },
        { name: 'velocidad_inicial1', label: 'Velocidad Inicial 1', unit: 'm/s', defaultValue: 10 },
        { name: 'angulo_inicial1_grados', label: 'Ángulo 1', unit: 'grados', defaultValue: 0 },
        { name: 'masa2', label: 'Masa 2', unit: 'kg', defaultValue: 5 },
        { name: 'velocidad_inicial2', label: 'Velocidad Inicial 2', unit: 'm/s', defaultValue: 10 },
        { name: 'angulo_inicial2_grados', label: 'Ángulo 2', unit: 'grados', defaultValue: 180 },
      ];
    case 'colision-elastica-3d':
      return [
        { name: 'masa1', label: 'Masa 1', unit: 'kg', defaultValue: 5 },
        { name: 'v1x', label: 'Vel Inicial 1 X', unit: 'm/s', defaultValue: 10 },
        { name: 'v1y', label: 'Vel Inicial 1 Y', unit: 'm/s', defaultValue: 0 },
        { name: 'v1z', label: 'Vel Inicial 1 Z', unit: 'm/s', defaultValue: 0 },
        { name: 'masa2', label: 'Masa 2', unit: 'kg', defaultValue: 5 },
        { name: 'v2x', label: 'Vel Inicial 2 X', unit: 'm/s', defaultValue: -10 },
        { name: 'v2y', label: 'Vel Inicial 2 Y', unit: 'm/s', defaultValue: 0 },
        { name: 'v2z', label: 'Vel Inicial 2 Z', unit: 'm/s', defaultValue: 0 },
      ];
    case 'colision-perfectamente-inelastica-2d':
      return [
        { name: 'masa1', label: 'Masa 1', unit: 'kg', defaultValue: 5 },
        { name: 'v1x', label: 'Vel Inicial 1 X', unit: 'm/s', defaultValue: 10 },
        { name: 'v1y', label: 'Vel Inicial 1 Y', unit: 'm/s', defaultValue: 0 },
        { name: 'masa2', label: 'Masa 2', unit: 'kg', defaultValue: 5 },
        { name: 'v2x', label: 'Vel Inicial 2 X', unit: 'm/s', defaultValue: 0 },
        { name: 'v2y', label: 'Vel Inicial 2 Y', unit: 'm/s', defaultValue: 10 },
      ];

    // Electricidad y Magnetismo
    case 'ley-ohm':
      return [
        { name: 'voltaje', label: 'Voltaje (Vacío si se desconoce)', unit: 'V', defaultValue: 12 },
        { name: 'corriente', label: 'Corriente (Vacío si se desconoce)', unit: 'A', defaultValue: undefined },
        { name: 'resistencia', label: 'Resistencia (Vacío si se desconoce)', unit: 'Ω', defaultValue: 4 },
      ];
    case 'resistencia':
      return [
        { name: 'resistividad', label: 'Resistividad del material', unit: 'Ω·m', defaultValue: 1.68e-8 },
        { name: 'longitud', label: 'Longitud', unit: 'm', defaultValue: 10 },
        { name: 'area', label: 'Área Transversal', unit: 'm²', defaultValue: 1e-6 },
      ];
    case 'potencia-electrica':
      return [
        { name: 'voltaje', label: 'Voltaje (Vacío si se desconoce)', unit: 'V', defaultValue: 12 },
        { name: 'corriente', label: 'Corriente (Vacío si se desconoce)', unit: 'A', defaultValue: 3 },
        { name: 'resistencia', label: 'Resistencia (Vacío si se desconoce)', unit: 'Ω', defaultValue: undefined },
      ];
    case 'capacitancia':
      return [
        { name: 'carga', label: 'Carga (Vacío si se desconoce)', unit: 'C', defaultValue: 0.001 },
        { name: 'voltaje', label: 'Voltaje (Vacío si se desconoce)', unit: 'V', defaultValue: 10 },
        { name: 'capacitancia', label: 'Capacitancia (Vacío si se desconoce)', unit: 'F', defaultValue: undefined },
      ];
    case 'inductancia':
      return [
        { name: 'flujo_magnetico', label: 'Flujo Magnético', unit: 'Wb', defaultValue: 0.05 },
        { name: 'corriente', label: 'Corriente', unit: 'A', defaultValue: 2 },
        { name: 'numero_espiras', label: 'Número de Espiras', unit: '', defaultValue: 100 },
      ];

    // Ondas
    case 'ondas':
      return [
        { name: 'frecuencia', label: 'Frecuencia (Hz) o Velocidad (m/s) o ...', unit: '', defaultValue: 50 },
        { name: 'longitud_onda', label: 'Longitud de Onda o Densidad...', unit: '', defaultValue: 2 },
      ];

    default:
      return [];
  }
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getOptionalParamsForSimulation = (_simSlug: string): ParamDefinition[] => {
  return [];
};

export const shouldDisplayChart = (simSlug: string): boolean => {
  const chartableSimulations = [
    'caida-libre',
    'tiro-parabolico',
    'plano-inclinado',
    'movimiento-circular-uniforme',
    'movimiento-armonico-simple',
    'pendulo-simple',
    'mru',
    'mruv',
    'leyes-newton',
    'fuerzas-leyes-newton',
  ];
  return chartableSimulations.includes(simSlug);
};