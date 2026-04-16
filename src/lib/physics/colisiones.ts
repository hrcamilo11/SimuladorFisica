// Colisiones - Cálculos de física

export function simularColisionElastica1D(masa1: number, velocidad_inicial1: number, masa2: number, velocidad_inicial2: number) {
  if (masa1 <= 0 || masa2 <= 0) throw new Error("Las masas deben ser positivas");

  // Conservation of momentum and kinetic energy
  const v1f = ((masa1 - masa2) * velocidad_inicial1 + 2 * masa2 * velocidad_inicial2) / (masa1 + masa2);
  const v2f = ((masa2 - masa1) * velocidad_inicial2 + 2 * masa1 * velocidad_inicial1) / (masa1 + masa2);

  const ke_inicial = 0.5 * masa1 * Math.pow(velocidad_inicial1, 2) + 0.5 * masa2 * Math.pow(velocidad_inicial2, 2);
  const ke_final = 0.5 * masa1 * Math.pow(v1f, 2) + 0.5 * masa2 * Math.pow(v2f, 2);
  const momentum_inicial = masa1 * velocidad_inicial1 + masa2 * velocidad_inicial2;
  const momentum_final = masa1 * v1f + masa2 * v2f;

  return {
    parametros_entrada: { masa1, velocidad_inicial1, masa2, velocidad_inicial2 },
    resultados: {
      velocidad_final1: Number(v1f.toFixed(4)),
      velocidad_final2: Number(v2f.toFixed(4)),
      energia_cinetica_inicial: Number(ke_inicial.toFixed(4)),
      energia_cinetica_final: Number(ke_final.toFixed(4)),
      momentum_inicial: Number(momentum_inicial.toFixed(4)),
      momentum_final: Number(momentum_final.toFixed(4)),
    },
    message: "Colisión elástica 1D calculada exitosamente."
  };
}

export function simularColisionElastica2D(
  masa1: number, velocidad_inicial1: number, angulo_inicial1_grados: number,
  masa2: number, velocidad_inicial2: number, angulo_inicial2_grados: number
) {
  const a1 = angulo_inicial1_grados * (Math.PI / 180);
  const a2 = angulo_inicial2_grados * (Math.PI / 180);

  const v1x = velocidad_inicial1 * Math.cos(a1);
  const v1y = velocidad_inicial1 * Math.sin(a1);
  const v2x = velocidad_inicial2 * Math.cos(a2);
  const v2y = velocidad_inicial2 * Math.sin(a2);

  // 1D elastic collision formula applied per axis
  const v1fx = ((masa1 - masa2) * v1x + 2 * masa2 * v2x) / (masa1 + masa2);
  const v1fy = ((masa1 - masa2) * v1y + 2 * masa2 * v2y) / (masa1 + masa2);
  const v2fx = ((masa2 - masa1) * v2x + 2 * masa1 * v1x) / (masa1 + masa2);
  const v2fy = ((masa2 - masa1) * v2y + 2 * masa1 * v1y) / (masa1 + masa2);

  const vel_final1 = Math.sqrt(v1fx * v1fx + v1fy * v1fy);
  const vel_final2 = Math.sqrt(v2fx * v2fx + v2fy * v2fy);
  const angulo_final1 = Math.atan2(v1fy, v1fx) * (180 / Math.PI);
  const angulo_final2 = Math.atan2(v2fy, v2fx) * (180 / Math.PI);

  return {
    parametros_entrada: { masa1, velocidad_inicial1, angulo_inicial1_grados, masa2, velocidad_inicial2, angulo_inicial2_grados },
    resultados: {
      velocidad_final1: Number(vel_final1.toFixed(4)),
      angulo_final1_grados: Number(angulo_final1.toFixed(4)),
      velocidad_final2: Number(vel_final2.toFixed(4)),
      angulo_final2_grados: Number(angulo_final2.toFixed(4)),
    },
    message: "Colisión elástica 2D calculada exitosamente."
  };
}

export function simularColisionElastica3D(
  masa1: number, v1x: number, v1y: number, v1z: number,
  masa2: number, v2x: number, v2y: number, v2z: number
) {
  const v1fx = ((masa1 - masa2) * v1x + 2 * masa2 * v2x) / (masa1 + masa2);
  const v1fy = ((masa1 - masa2) * v1y + 2 * masa2 * v2y) / (masa1 + masa2);
  const v1fz = ((masa1 - masa2) * v1z + 2 * masa2 * v2z) / (masa1 + masa2);
  const v2fx = ((masa2 - masa1) * v2x + 2 * masa1 * v1x) / (masa1 + masa2);
  const v2fy = ((masa2 - masa1) * v2y + 2 * masa1 * v1y) / (masa1 + masa2);
  const v2fz = ((masa2 - masa1) * v2z + 2 * masa1 * v1z) / (masa1 + masa2);

  return {
    parametros_entrada: { masa1, v1x, v1y, v1z, masa2, v2x, v2y, v2z },
    resultados: {
      velocidad_final1: { x: Number(v1fx.toFixed(4)), y: Number(v1fy.toFixed(4)), z: Number(v1fz.toFixed(4)) },
      velocidad_final2: { x: Number(v2fx.toFixed(4)), y: Number(v2fy.toFixed(4)), z: Number(v2fz.toFixed(4)) },
      magnitud_vel_final1: Number(Math.sqrt(v1fx ** 2 + v1fy ** 2 + v1fz ** 2).toFixed(4)),
      magnitud_vel_final2: Number(Math.sqrt(v2fx ** 2 + v2fy ** 2 + v2fz ** 2).toFixed(4)),
    },
    message: "Colisión elástica 3D calculada exitosamente."
  };
}

export function simularColisionInelastica1D(masa1: number, velocidad_inicial1: number, masa2: number, velocidad_inicial2: number) {
  if (masa1 <= 0 || masa2 <= 0) throw new Error("Las masas deben ser positivas");

  const vf = (masa1 * velocidad_inicial1 + masa2 * velocidad_inicial2) / (masa1 + masa2);
  const ke_inicial = 0.5 * masa1 * Math.pow(velocidad_inicial1, 2) + 0.5 * masa2 * Math.pow(velocidad_inicial2, 2);
  const ke_final = 0.5 * (masa1 + masa2) * Math.pow(vf, 2);
  const energia_perdida = ke_inicial - ke_final;

  return {
    parametros_entrada: { masa1, velocidad_inicial1, masa2, velocidad_inicial2 },
    resultados: {
      velocidad_final: Number(vf.toFixed(4)),
      energia_cinetica_inicial: Number(ke_inicial.toFixed(4)),
      energia_cinetica_final: Number(ke_final.toFixed(4)),
      energia_perdida: Number(energia_perdida.toFixed(4)),
    },
    message: "Colisión perfectamente inelástica 1D calculada exitosamente."
  };
}

export function simularColisionInelastica2D(
  masa1: number, v1x: number, v1y: number,
  masa2: number, v2x: number, v2y: number
) {
  const vfx = (masa1 * v1x + masa2 * v2x) / (masa1 + masa2);
  const vfy = (masa1 * v1y + masa2 * v2y) / (masa1 + masa2);
  const vel_final = Math.sqrt(vfx * vfx + vfy * vfy);
  const angulo_final = Math.atan2(vfy, vfx) * (180 / Math.PI);

  return {
    parametros_entrada: { masa1, v1x, v1y, masa2, v2x, v2y },
    resultados: {
      velocidad_final_x: Number(vfx.toFixed(4)),
      velocidad_final_y: Number(vfy.toFixed(4)),
      magnitud_velocidad_final: Number(vel_final.toFixed(4)),
      angulo_final_grados: Number(angulo_final.toFixed(4)),
    },
    message: "Colisión perfectamente inelástica 2D calculada exitosamente."
  };
}
