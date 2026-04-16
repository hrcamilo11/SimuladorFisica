// Dinámica - Cálculos de física
const GRAVEDAD = 9.81;

export function simularLeyesNewton(masa: number, fuerza_aplicada: number, coeficiente_rozamiento: number = 0, tiempo_total_simulacion: number = 5, num_puntos: number = 100) {
  if (masa <= 0) throw new Error("La masa debe ser positiva");

  const fuerza_normal = masa * GRAVEDAD;
  const fuerza_rozamiento = coeficiente_rozamiento * fuerza_normal;
  const fuerza_neta = fuerza_aplicada - fuerza_rozamiento;
  const aceleracion = fuerza_neta / masa;

  const estados_simulacion = [];
  const paso = tiempo_total_simulacion / (num_puntos - 1);

  for (let i = 0; i < num_puntos; i++) {
    const t = i * paso;
    const v = aceleracion * t;
    const x = 0.5 * aceleracion * t * t;
    estados_simulacion.push({
      tiempo: Number(t.toFixed(4)),
      posicion: Number(x.toFixed(4)),
      velocidad: Number(v.toFixed(4)),
      aceleracion: Number(aceleracion.toFixed(4)),
    });
  }

  return {
    parametros_entrada: { masa, fuerza_aplicada, coeficiente_rozamiento },
    resultados: {
      fuerza_neta: Number(fuerza_neta.toFixed(4)),
      aceleracion: Number(aceleracion.toFixed(4)),
      fuerza_normal: Number(fuerza_normal.toFixed(4)),
      fuerza_rozamiento: Number(fuerza_rozamiento.toFixed(4)),
      estados_simulacion,
    },
    message: "Simulación de Leyes de Newton calculada exitosamente."
  };
}

export function simularPlanoInclinado(masa: number, angulo_grados: number, coeficiente_rozamiento: number = 0, distancia: number = 10, velocidad_inicial: number = 0, tiempo_total_simulacion: number = 5, num_puntos: number = 100) {
  if (masa <= 0) throw new Error("La masa debe ser positiva");
  const angulo = angulo_grados * (Math.PI / 180);

  const fuerza_normal = masa * GRAVEDAD * Math.cos(angulo);
  const fuerza_gravedad_paralela = masa * GRAVEDAD * Math.sin(angulo);
  const fuerza_rozamiento = coeficiente_rozamiento * fuerza_normal;
  const fuerza_neta = fuerza_gravedad_paralela - fuerza_rozamiento;
  const aceleracion = fuerza_neta / masa;

  const estados_simulacion = [];
  const paso = tiempo_total_simulacion / (num_puntos - 1);

  for (let i = 0; i < num_puntos; i++) {
    const t = i * paso;
    const s = velocidad_inicial * t + 0.5 * aceleracion * t * t;
    const v = velocidad_inicial + aceleracion * t;
    const x = s * Math.cos(angulo);
    const y = -s * Math.sin(angulo); // negative because going down

    if (s <= distancia && s >= 0) {
      estados_simulacion.push({
        tiempo: Number(t.toFixed(4)),
        posicion: Number(s.toFixed(4)),
        posicion_x: Number(x.toFixed(4)),
        posicion_y: Number(y.toFixed(4)),
        velocidad: Number(v.toFixed(4)),
      });
    }
  }

  return {
    parametros_entrada: { masa, angulo_grados, coeficiente_rozamiento, distancia },
    resultados: {
      fuerza_normal: Number(fuerza_normal.toFixed(4)),
      fuerza_gravedad_paralela: Number(fuerza_gravedad_paralela.toFixed(4)),
      fuerza_rozamiento: Number(fuerza_rozamiento.toFixed(4)),
      fuerza_neta: Number(fuerza_neta.toFixed(4)),
      aceleracion: Number(aceleracion.toFixed(4)),
      estados_simulacion,
    },
    message: "Simulación de plano inclinado calculada exitosamente."
  };
}

export function simularPlanoInclinadoPolea(masa1: number, masa2: number, angulo_grados: number, coeficiente_rozamiento_estatico: number, coeficiente_rozamiento_cinetico: number) {
  if (masa1 <= 0 || masa2 <= 0) throw new Error("Las masas deben ser positivas");
  const angulo = angulo_grados * (Math.PI / 180);

  const fuerza_normal = masa1 * GRAVEDAD * Math.cos(angulo);
  const componente_paralela = masa1 * GRAVEDAD * Math.sin(angulo);
  const fuerza_rozamiento_max = coeficiente_rozamiento_estatico * fuerza_normal;
  const fuerza_peso2 = masa2 * GRAVEDAD;

  const fuerza_neta_sin_rozamiento = fuerza_peso2 - componente_paralela;
  const se_mueve = Math.abs(fuerza_neta_sin_rozamiento) > fuerza_rozamiento_max;

  let aceleracion = 0;
  let tension = 0;

  if (se_mueve) {
    const fuerza_rozamiento_cinetico = coeficiente_rozamiento_cinetico * fuerza_normal;
    if (fuerza_peso2 > componente_paralela) {
      aceleracion = (fuerza_peso2 - componente_paralela - fuerza_rozamiento_cinetico) / (masa1 + masa2);
    } else {
      aceleracion = (fuerza_peso2 - componente_paralela + fuerza_rozamiento_cinetico) / (masa1 + masa2);
    }
    tension = masa2 * (GRAVEDAD - aceleracion);
  } else {
    tension = fuerza_peso2;
  }

  return {
    parametros_entrada: { masa1, masa2, angulo_grados, coeficiente_rozamiento_estatico, coeficiente_rozamiento_cinetico },
    resultados: {
      aceleracion: Number(aceleracion.toFixed(4)),
      tension: Number(tension.toFixed(4)),
      fuerza_normal: Number(fuerza_normal.toFixed(4)),
      se_mueve,
    },
    message: "Simulación de plano inclinado con polea calculada exitosamente."
  };
}
