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
      return [
        { formula: 'F_n = mg cos(θ)', description: 'Fuerza normal en plano inclinado' },
        { formula: 'F_g_x = mg sen(θ)', description: 'Componente de la gravedad paralela al plano' }
      ];
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
    'fuerzas-leyes-newton',
    'energia-potencial-conservacion',
    'energia-potencial-elastica',
  ];
  return chartableSimulations.includes(simSlug);
};

export const formatDataForChart = (simulationData: { resultados: SimulationResult }, simSlug: string): ChartDataPoint[] => {
  const resultados = simulationData.resultados;
  if (resultados.estados_simulacion && resultados.estados_simulacion.length > 0) {
    return resultados.estados_simulacion.map((estado: any) => {
      const chartPoint: ChartDataPoint = { tiempo: estado.tiempo };
      for (const key in estado) {
        if (key !== 'tiempo') {
          chartPoint[key] = estado[key];
        }
      }
      return chartPoint;
    });
  } else {
    const tiempos = resultados.tiempos || [];
    const posiciones = resultados.posiciones || [];
    const velocidades = resultados.velocidades || [];
    const aceleraciones = resultados.aceleraciones || [];
    let data: ChartDataPoint[] = [];

    switch (simSlug) {
      case 'caida-libre':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          posicion: posiciones[i] || 0,
          velocidad: velocidades[i] || 0,
          aceleracion: aceleraciones[i] || 0
        }));
        break;
      case 'tiro-parabolico':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          posicion_x: resultados.posiciones_x?.[i] || 0,
          posicion_y: resultados.posiciones_y?.[i] || 0,
          velocidad_x: resultados.velocidades_x?.[i] || 0,
          velocidad_y: resultados.velocidades_y?.[i] || 0,
          aceleracion_x: resultados.aceleraciones_x?.[i] || 0,
          aceleracion_y: resultados.aceleraciones_y?.[i] || 0,
        }));
        break;
      case 'plano-inclinado':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          posicion_x: resultados.posiciones_x?.[i] || 0,
          posicion_y: resultados.posiciones_y?.[i] || 0,
          velocidad_x: resultados.velocidades_x?.[i] || 0,
          velocidad_y: resultados.velocidades_y?.[i] || 0,
          aceleracion_x: resultados.aceleraciones_x?.[i] || 0,
          aceleracion_y: resultados.aceleraciones_y?.[i] || 0,
          fuerza: resultados.fuerzas?.[i] || 0,
        }));
        break;
      case 'movimiento-circular-uniforme':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          posicion_x: resultados.posiciones_x?.[i] || 0,
          posicion_y: resultados.posiciones_y?.[i] || 0,
          angulo: resultados.angulos?.[i] || 0,
        }));
        break;
      case 'movimiento-armonico-simple':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          posicion_x: resultados.posiciones?.[i] || 0,
          velocidad_x: resultados.velocidades?.[i] || 0,
          aceleracion_x: resultados.aceleraciones?.[i] || 0,
        }));
        break;
      case 'pendulo-simple':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          posicion_angular: resultados.posiciones_angular?.[i] || 0,
          velocidad_angular: resultados.velocidades_angular?.[i] || 0,
          aceleracion_angular: resultados.aceleraciones_angular?.[i] || 0,
          posicion_x_cartesiana: resultados.posiciones_x_cartesianas?.[i] || 0,
          posicion_y_cartesiana: resultados.posiciones_y_cartesianas?.[i] || 0,
        }));
        break;
      case 'mru':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          posicion: posiciones[i] || 0,
          velocidad: velocidades[i] || 0,
        }));
        break;
      case 'mruv':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          posicion: posiciones[i] || 0,
          velocidad: velocidades[i] || 0,
          aceleracion: aceleraciones[i] || 0,
        }));
        break;
      case 'fuerzas-leyes-newton':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          fuerza: resultados.fuerzas?.[i] || 0,
          aceleracion: resultados.aceleraciones?.[i] || 0,
        }));
        break;
      case 'energia-potencial-conservacion':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          energia_cinetica: resultados.energias_cineticas?.[i] || 0,
          energia_potencial: resultados.energias_potenciales?.[i] || 0,
          energia_total: resultados.energias_totales?.[i] || 0,
        }));
        break;
      case 'energia-potencial-elastica':
        data = tiempos.map((t, i) => ({
          tiempo: t,
          energia_potencial_elastica: resultados.energias_potenciales_elasticas?.[i] || 0,
          posicion: resultados.posiciones?.[i] || 0,
        }));
        break;
      default:
        data = tiempos.map((t, i) => ({
          tiempo: t,
          posicion: posiciones[i] || 0,
        }));
        break;
    }
    return data;
  }
};

export const getExpectedParamsForSimulation = (simSlug: string): ParamDefinition[] => {
  switch (simSlug) {
    case 'caida-libre':
      return [
        { name: 'altura_inicial', label: 'Altura Inicial', unit: 'm' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'mru':
      return [
        { name: 'posicion_inicial', label: 'Posición Inicial', unit: 'm' },
        { name: 'velocidad', label: 'Velocidad', unit: 'm/s' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'mruv':
      return [
        { name: 'posicion_inicial', label: 'Posición Inicial', unit: 'm' },
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
        { name: 'aceleracion', label: 'Aceleración', unit: 'm/s²' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'tiro-parabolico':
      return [
        { name: 'altura_inicial', label: 'Altura Inicial', unit: 'm' },
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
        { name: 'angulo_lanzamiento', label: 'Ángulo de Lanzamiento', unit: 'grados' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'plano-inclinado':
      return [
        { name: 'masa', label: 'Masa', unit: 'kg' },
        { name: 'angulo_inclinacion', label: 'Ángulo de Inclinación', unit: 'grados' },
        { name: 'coeficiente_rozamiento_cinetico', label: 'Coeficiente de Rozamiento Cinético', unit: '' },
        { name: 'distancia_recorrida', label: 'Distancia Recorrida', unit: 'm' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'movimiento-circular-uniforme':
      return [
        { name: 'radio', label: 'Radio', unit: 'm' },
        { name: 'velocidad_angular', label: 'Velocidad Angular', unit: 'rad/s' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'movimiento-armonico-simple':
      return [
        { name: 'amplitud', label: 'Amplitud', unit: 'm' },
        { name: 'frecuencia_angular', label: 'Frecuencia Angular', unit: 'rad/s' },
        { name: 'fase_inicial', label: 'Fase Inicial', unit: 'rad' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'pendulo-simple':
      return [
        { name: 'longitud', label: 'Longitud del Hilo', unit: 'm' },
        { name: 'angulo_inicial', label: 'Ángulo Inicial', unit: 'grados' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'fuerzas-leyes-newton':
      return [
        { name: 'masa', label: 'Masa', unit: 'kg' },
        { name: 'fuerza_aplicada', label: 'Fuerza Aplicada', unit: 'N' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'energia-potencial-conservacion':
      return [
        { name: 'masa', label: 'Masa', unit: 'kg' },
        { name: 'altura_inicial', label: 'Altura Inicial', unit: 'm' },
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    case 'energia-potencial-elastica':
      return [
        { name: 'constante_elastica', label: 'Constante Elástica (k)', unit: 'N/m' },
        { name: 'desplazamiento', label: 'Desplazamiento (x)', unit: 'm' },
        { name: 'tiempo_total_simulacion', label: 'Tiempo Total de Simulación', unit: 's' },
        { name: 'num_puntos', label: 'Número de Puntos', unit: '' },
      ];
    default:
      return [];
  }
};

export const getOptionalParamsForSimulation = (simSlug: string): ParamDefinition[] => {
  switch (simSlug) {
    case 'caida-libre':
      return [
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
      ];
    case 'mru':
      return [];
    case 'mruv':
      return [];
    case 'tiro-parabolico':
      return [];
    case 'plano-inclinado':
      return [
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
      ];
    case 'movimiento-circular-uniforme':
      return [
        { name: 'posicion_angular_inicial', label: 'Posición Angular Inicial', unit: 'rad' },
      ];
    case 'movimiento-armonico-simple':
      return [
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
      ];
    case 'pendulo-simple':
      return [
        { name: 'velocidad_angular_inicial', label: 'Velocidad Angular Inicial', unit: 'rad/s' },
      ];
    case 'fuerzas-leyes-newton':
      return [
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
      ];
    case 'energia-potencial-conservacion':
      return [];
    case 'energia-potencial-elastica':
      return [
        { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
      ];
    default:
      return [];
  }
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
    'fuerzas-leyes-newton',
    'energia-potencial-conservacion',
    'energia-potencial-elastica',
  ];
  return chartableSimulations.includes(simSlug);
};