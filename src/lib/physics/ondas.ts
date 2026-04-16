// Ondas - Cálculos de física

export function simularOndas(tipo_calculo: string, params: Record<string, number>) {
  switch (tipo_calculo) {
    case 'velocidad_onda': {
      const v = params.frecuencia * params.longitud_onda;
      return {
        parametros_entrada: params,
        resultados: { velocidad: Number(v.toFixed(4)) },
        message: "Velocidad de onda calculada exitosamente."
      };
    }
    case 'frecuencia_onda': {
      const f = params.velocidad / params.longitud_onda;
      return {
        parametros_entrada: params,
        resultados: { frecuencia: Number(f.toFixed(4)), periodo: Number((1 / f).toFixed(6)) },
        message: "Frecuencia de onda calculada exitosamente."
      };
    }
    case 'longitud_onda': {
      const lambda = params.velocidad / params.frecuencia;
      return {
        parametros_entrada: params,
        resultados: { longitud_onda: Number(lambda.toFixed(4)) },
        message: "Longitud de onda calculada exitosamente."
      };
    }
    case 'periodo_onda': {
      const T = 1 / params.frecuencia;
      return {
        parametros_entrada: params,
        resultados: { periodo: Number(T.toFixed(6)) },
        message: "Período de onda calculado exitosamente."
      };
    }
    case 'velocidad_cuerda': {
      const v = Math.sqrt(params.tension / params.densidad_lineal);
      return {
        parametros_entrada: params,
        resultados: { velocidad: Number(v.toFixed(4)) },
        message: "Velocidad en cuerda calculada exitosamente."
      };
    }
    default:
      throw new Error(`Tipo de cálculo no válido: ${tipo_calculo}`);
  }
}
