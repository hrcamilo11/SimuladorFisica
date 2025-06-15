export interface SimulationParams {
  [key: string]: any;
}

export interface SimulationResult {
  [key: string]: any;
  tiempos?: number[];
  posiciones?: number[];
  alturas?: number[];
  velocidades?: number[];
  posiciones_x?: number[];
  posiciones_y?: number[];
  angulos?: number[];
  velocidades_x?: number[];
  velocidades_y?: number[];
  aceleraciones?: number[];
  energias_potenciales?: number[];
  energias_cineticas?: number[];
  energias_totales?: number[];
  posiciones_angular?: number[];
  velocidades_angular?: number[];
  aceleraciones_angular?: number[];
  posiciones_x_cartesianas?: number[];
  posiciones_y_cartesianas?: number[];
  estados_simulacion?: any[];
}

export interface ChartDataPoint {
  tiempo: number;
  [key: string]: number;
}

export interface SimulationData {
  tipo_simulacion: string;
  parametros_entrada: SimulationParams;
  resultados: SimulationResult;
  mensaje?: string;
  error?: string;
}

export interface ParamDefinition {
  name: string;
  label: string;
  unit?: string;
}

export interface Formula {
  formula: string;
  description?: string;
}

export interface SimulationPageProps {
  params: Promise<{
    slug: string;
  }>;
}