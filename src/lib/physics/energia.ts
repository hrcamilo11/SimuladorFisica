// Energía - Cálculos de física
const GRAVEDAD = 9.81;

export function simularTrabajoEnergia(masa: number, velocidad_inicial: number, velocidad_final: number) {
  if (masa <= 0) throw new Error("La masa debe ser positiva");

  const ke_inicial = 0.5 * masa * Math.pow(velocidad_inicial, 2);
  const ke_final = 0.5 * masa * Math.pow(velocidad_final, 2);
  const trabajo = ke_final - ke_inicial;

  return {
    parametros_entrada: { masa, velocidad_inicial, velocidad_final },
    resultados: {
      energia_cinetica_inicial: Number(ke_inicial.toFixed(4)),
      energia_cinetica_final: Number(ke_final.toFixed(4)),
      trabajo_neto: Number(trabajo.toFixed(4)),
    },
    message: "Cálculo de trabajo y energía cinética exitoso."
  };
}

export function simularEnergiaPotencialGravitatoria(masa: number, altura: number) {
  if (masa <= 0) throw new Error("La masa debe ser positiva");

  const ep = masa * GRAVEDAD * altura;
  const velocidad_caida = Math.sqrt(2 * GRAVEDAD * Math.abs(altura));

  return {
    parametros_entrada: { masa, altura },
    resultados: {
      energia_potencial: Number(ep.toFixed(4)),
      velocidad_equivalente_caida: Number(velocidad_caida.toFixed(4)),
    },
    message: "Cálculo de energía potencial gravitatoria exitoso."
  };
}

export function simularEnergiaPotencialElastica(constante_elastica: number, deformacion: number) {
  if (constante_elastica <= 0) throw new Error("La constante elástica debe ser positiva");

  const ep = 0.5 * constante_elastica * Math.pow(deformacion, 2);
  const fuerza = constante_elastica * Math.abs(deformacion);

  return {
    parametros_entrada: { constante_elastica, deformacion },
    resultados: {
      energia_potencial_elastica: Number(ep.toFixed(4)),
      fuerza_resorte: Number(fuerza.toFixed(4)),
    },
    message: "Cálculo de energía potencial elástica exitoso."
  };
}
