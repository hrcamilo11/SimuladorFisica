// Electricidad y Magnetismo - Cálculos de física
const MU_0 = 4 * Math.PI * 1e-7; // Permeabilidad del vacío
const EPSILON_0 = 8.854e-12; // Permitividad del vacío
const K_COULOMB = 1 / (4 * Math.PI * EPSILON_0);

export function simularLeyOhm(voltaje?: number, corriente?: number, resistencia?: number) {
  let v = voltaje, i = corriente, r = resistencia;

  if (v !== undefined && i !== undefined) {
    r = v / i;
  } else if (v !== undefined && r !== undefined) {
    i = v / r;
  } else if (i !== undefined && r !== undefined) {
    v = i * r;
  } else {
    throw new Error("Se necesitan al menos dos de los tres valores: voltaje, corriente, resistencia");
  }

  return {
    parametros_entrada: { voltaje, corriente, resistencia },
    resultados: { voltaje: Number(v!.toFixed(4)), corriente: Number(i!.toFixed(4)), resistencia: Number(r!.toFixed(4)), potencia: Number((v! * i!).toFixed(4)) },
    message: "Cálculo de Ley de Ohm exitoso."
  };
}

export function simularResistencia(resistividad: number, longitud: number, area: number) {
  if (area <= 0) throw new Error("El área debe ser positiva");
  const R = resistividad * longitud / area;
  const conductancia = 1 / R;

  return {
    parametros_entrada: { resistividad, longitud, area },
    resultados: { resistencia: Number(R.toFixed(6)), conductancia: Number(conductancia.toFixed(6)) },
    message: "Cálculo de resistencia por material exitoso."
  };
}

export function simularCircuitoSerie(resistencias: number[], voltaje_total: number) {
  const resistencia_total = resistencias.reduce((a, b) => a + b, 0);
  const corriente = voltaje_total / resistencia_total;
  const voltajes = resistencias.map(r => Number((corriente * r).toFixed(4)));

  return {
    parametros_entrada: { resistencias, voltaje_total },
    resultados: { resistencia_total: Number(resistencia_total.toFixed(4)), corriente: Number(corriente.toFixed(4)), voltajes_individuales: voltajes },
    message: "Cálculo de circuito en serie exitoso."
  };
}

export function simularCircuitoParalelo(resistencias: number[], voltaje_total: number) {
  const inv_total = resistencias.reduce((a, r) => a + 1 / r, 0);
  const resistencia_total = 1 / inv_total;
  const corriente_total = voltaje_total / resistencia_total;
  const corrientes = resistencias.map(r => Number((voltaje_total / r).toFixed(4)));

  return {
    parametros_entrada: { resistencias, voltaje_total },
    resultados: { resistencia_total: Number(resistencia_total.toFixed(4)), corriente_total: Number(corriente_total.toFixed(4)), corrientes_individuales: corrientes },
    message: "Cálculo de circuito en paralelo exitoso."
  };
}

export function simularPotenciaElectrica(voltaje?: number, corriente?: number, resistencia?: number) {
  let potencia: number;

  if (voltaje !== undefined && corriente !== undefined) {
    potencia = voltaje * corriente;
  } else if (voltaje !== undefined && resistencia !== undefined) {
    potencia = Math.pow(voltaje, 2) / resistencia;
  } else if (corriente !== undefined && resistencia !== undefined) {
    potencia = Math.pow(corriente, 2) * resistencia;
  } else {
    throw new Error("Se necesitan al menos dos valores");
  }

  return {
    parametros_entrada: { voltaje, corriente, resistencia },
    resultados: { potencia: Number(potencia.toFixed(4)) },
    message: "Cálculo de potencia eléctrica exitoso."
  };
}

export function simularCapacitancia(carga?: number, voltaje?: number, capacitancia?: number) {
  let c = capacitancia, q = carga, v = voltaje;

  if (q !== undefined && v !== undefined) {
    c = q / v;
  } else if (q !== undefined && c !== undefined) {
    v = q / c;
  } else if (v !== undefined && c !== undefined) {
    q = c * v;
  } else {
    throw new Error("Se necesitan al menos dos valores");
  }

  const energia = 0.5 * c! * Math.pow(v!, 2);

  return {
    parametros_entrada: { carga, voltaje, capacitancia },
    resultados: { capacitancia: Number(c!.toFixed(6)), carga: Number(q!.toFixed(6)), voltaje: Number(v!.toFixed(4)), energia_almacenada: Number(energia.toFixed(6)) },
    message: "Cálculo de capacitancia exitoso."
  };
}

export function simularInductancia(flujo_magnetico: number, corriente: number, numero_espiras: number) {
  if (corriente === 0) throw new Error("La corriente no puede ser cero");
  const inductancia = numero_espiras * flujo_magnetico / corriente;
  const energia = 0.5 * inductancia * Math.pow(corriente, 2);

  return {
    parametros_entrada: { flujo_magnetico, corriente, numero_espiras },
    resultados: { inductancia: Number(inductancia.toFixed(6)), energia_almacenada: Number(energia.toFixed(6)) },
    message: "Cálculo de inductancia exitoso."
  };
}

export function simularMagnetismo(tipo_calculo: string, params: Record<string, number>) {
  switch (tipo_calculo) {
    case 'campo_magnetico': {
      const B = (MU_0 * params.corriente) / (2 * Math.PI * params.distancia);
      return { resultados: { campo_magnetico: Number(B.toFixed(8)) }, message: "Campo magnético calculado." };
    }
    case 'flujo_magnetico': {
      const phi = params.campo_magnetico * params.area * Math.cos(params.angulo * Math.PI / 180);
      return { resultados: { flujo_magnetico: Number(phi.toFixed(8)) }, message: "Flujo magnético calculado." };
    }
    case 'fuerza_lorentz': {
      const F = params.carga * params.velocidad * params.campo_magnetico * Math.sin(params.angulo * Math.PI / 180);
      return { resultados: { fuerza_lorentz: Number(F.toFixed(8)) }, message: "Fuerza de Lorentz calculada." };
    }
    case 'ley_faraday': {
      const emf = -params.num_espiras * params.cambio_flujo / params.cambio_tiempo;
      return { resultados: { fem_inducida: Number(emf.toFixed(6)) }, message: "FEM inducida calculada." };
    }
    default:
      throw new Error(`Tipo de cálculo no válido: ${tipo_calculo}`);
  }
}

export function simularLeyesKirchhoff(tipo: string, params: Record<string, number[]>) {
  if (tipo === 'voltaje') {
    const voltajes = params.voltajes || [];
    const suma = voltajes.reduce((a, b) => a + b, 0);
    return { resultados: { suma_voltajes: Number(suma.toFixed(4)), cumple_ley: Math.abs(suma) < 0.001 }, message: "Ley de Kirchhoff de voltaje calculada." };
  } else {
    const entrantes = params.corrientes_entrantes || [];
    const salientes = params.corrientes_salientes || [];
    const suma_entrantes = entrantes.reduce((a, b) => a + b, 0);
    const suma_salientes = salientes.reduce((a, b) => a + b, 0);
    return { resultados: { suma_entrantes: Number(suma_entrantes.toFixed(4)), suma_salientes: Number(suma_salientes.toFixed(4)), cumple_ley: Math.abs(suma_entrantes - suma_salientes) < 0.001 }, message: "Ley de Kirchhoff de corriente calculada." };
  }
}

export { K_COULOMB, EPSILON_0, MU_0 };
