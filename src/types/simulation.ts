export interface SimulationParams {
  [key: string]: number | undefined;
}

export interface SimulationResult {
  [key: string]: number | number[] | Record<string, unknown>[] | undefined;
  tiempos?: number[];
  posiciones?: number[];
  alturas?: number[];
  velocidades?: number[];
  posiciones_x?: number[];
  posiciones_y?: number[];
  angulos?: number[];
  velocidades_x?: number[];
  velocidades_y?: number[];
  aceleraciones_x?: number[];
  aceleraciones_y?: number[];
  aceleraciones?: number[];
  fuerzas?: number[];
  energias_potenciales_elasticas?: number[];
  energias_potenciales?: number[];
  energias_cineticas?: number[];
  energias_totales?: number[];
  posiciones_angular?: number[];
  velocidades_angular?: number[];
  aceleraciones_angular?: number[];
  posiciones_x_cartesianas?: number[];
  posiciones_y_cartesianas?: number[];
  estados_simulacion?: Record<string, unknown>[];
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
  defaultValue?: number;
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