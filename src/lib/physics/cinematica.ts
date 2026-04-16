const GRAVEDAD = 9.81; // m/s^2

export function simularCaidaLibre(altura_inicial: number, tiempo_total_simulacion?: number | null, num_puntos: number = 100) {
  if (altura_inicial <= 0) throw new Error("La altura inicial debe ser mayor a 0");

  const tiempo_hasta_suelo = Math.sqrt((2 * altura_inicial) / GRAVEDAD);
  const tiempo_total = tiempo_total_simulacion || tiempo_hasta_suelo;

  const estados_simulacion = [];
  const paso_tiempo = tiempo_total / (num_puntos - 1);

  for (let i = 0; i < num_puntos; i++) {
    const t = i * paso_tiempo;
    const h = altura_inicial - 0.5 * GRAVEDAD * Math.pow(t, 2);
    const v = -GRAVEDAD * t;

    if (h >= 0) {
      estados_simulacion.push({ tiempo: Number(t.toFixed(4)), altura: Number(h.toFixed(4)), velocidad: Number(v.toFixed(4)) });
    } else {
      // Add exact impact point
      estados_simulacion.push({
        tiempo: Number(tiempo_hasta_suelo.toFixed(4)),
        altura: 0,
        velocidad: Number((-GRAVEDAD * tiempo_hasta_suelo).toFixed(4))
      });
      break;
    }
  }

  return {
    parametros_entrada: { altura_inicial, tiempo_total_simulacion },
    resultados: {
      tiempo_total_simulacion: tiempo_total,
      estados_simulacion
    },
    message: "Simulación de caída libre calculada exitosamente."
  };
}

export function simularMRU(posicion_inicial: number, velocidad: number, tiempo_total_simulacion: number, num_puntos: number = 100) {
  if (tiempo_total_simulacion <= 0) throw new Error("El tiempo debe ser mayor a 0");

  const estados_simulacion = [];
  const paso_tiempo = tiempo_total_simulacion / (num_puntos - 1);

  for (let i = 0; i < num_puntos; i++) {
    const t = i * paso_tiempo;
    const x = posicion_inicial + velocidad * t;

    estados_simulacion.push({
      tiempo: Number(t.toFixed(4)),
      posicion: Number(x.toFixed(4)),
      velocidad: Number(velocidad.toFixed(4))
    });
  }

  return {
    parametros_entrada: { posicion_inicial, velocidad, tiempo_total_simulacion },
    resultados: {
      tiempo_total_simulacion,
      estados_simulacion
    },
    message: "Simulación de MRU calculada exitosamente."
  };
}

export function simularMRUV(posicion_inicial: number, velocidad_inicial: number, aceleracion: number, tiempo_total_simulacion: number, num_puntos: number = 100) {
  if (tiempo_total_simulacion <= 0) throw new Error("El tiempo debe ser mayor a 0");

  const estados_simulacion = [];
  const paso_tiempo = tiempo_total_simulacion / (num_puntos - 1);

  for (let i = 0; i < num_puntos; i++) {
    const t = i * paso_tiempo;
    const x = posicion_inicial + velocidad_inicial * t + 0.5 * aceleracion * Math.pow(t, 2);
    const v = velocidad_inicial + aceleracion * t;

    estados_simulacion.push({
      tiempo: Number(t.toFixed(4)),
      posicion: Number(x.toFixed(4)),
      velocidad: Number(v.toFixed(4)),
      aceleracion: Number(aceleracion.toFixed(4))
    });
  }

  return {
    parametros_entrada: { posicion_inicial, velocidad_inicial, aceleracion, tiempo_total_simulacion },
    resultados: {
      tiempo_total_simulacion,
      estados_simulacion
    },
    message: "Simulación de MRUV calculada exitosamente."
  };
}

export function simularTiroParabolico(velocidad_inicial: number, angulo_grados: number, altura_inicial: number = 0, tiempo_total_simulacion?: number | null, num_puntos: number = 100) {
  if (velocidad_inicial < 0) throw new Error("La velocidad inicial debe ser no negativa");
  
  const angulo_rad = angulo_grados * (Math.PI / 180);
  const v0x = velocidad_inicial * Math.cos(angulo_rad);
  const v0y = velocidad_inicial * Math.sin(angulo_rad);

  // Time of flight: y = y0 + v0y*t - 0.5*g*t^2 = 0
  let tiempo_vuelo = 0;
  if (altura_inicial === 0) {
    tiempo_vuelo = (2 * v0y) / GRAVEDAD;
  } else {
    // Quadratic equation: -0.5*g*t^2 + v0y*t + y0 = 0
    const a = -0.5 * GRAVEDAD;
    const b = v0y;
    const c = altura_inicial;
    const discriminant = Math.pow(b, 2) - 4 * a * c;
    if (discriminant >= 0) {
      const t1 = (-b + Math.sqrt(discriminant)) / (2 * a);
      const t2 = (-b - Math.sqrt(discriminant)) / (2 * a);
      tiempo_vuelo = Math.max(t1, t2);
    }
  }

  const tiempo_total = tiempo_total_simulacion || tiempo_vuelo;
  const estados_simulacion = [];
  const paso_tiempo = tiempo_total / (num_puntos - 1);

  for (let i = 0; i < num_puntos; i++) {
    const t = i * paso_tiempo;
    const x = v0x * t;
    const y = altura_inicial + v0y * t - 0.5 * GRAVEDAD * Math.pow(t, 2);
    const vx = v0x;
    const vy = v0y - GRAVEDAD * t;

    if (y >= 0) {
      estados_simulacion.push({
        tiempo: Number(t.toFixed(4)),
        posicion_x: Number(x.toFixed(4)),
        posicion_y: Number(y.toFixed(4)),
        velocidad_x: Number(vx.toFixed(4)),
        velocidad_y: Number(vy.toFixed(4))
      });
    } else {
      // Add exact impact point
      estados_simulacion.push({
        tiempo: Number(tiempo_vuelo.toFixed(4)),
        posicion_x: Number((v0x * tiempo_vuelo).toFixed(4)),
        posicion_y: 0,
        velocidad_x: Number(v0x.toFixed(4)),
        velocidad_y: Number((v0y - GRAVEDAD * tiempo_vuelo).toFixed(4))
      });
      break;
    }
  }

  return {
    parametros_entrada: { velocidad_inicial, angulo_grados, altura_inicial, tiempo_total_simulacion },
    resultados: {
      tiempo_total_simulacion: tiempo_total,
      estados_simulacion,
      tiempo_vuelo: Number(tiempo_vuelo.toFixed(4)),
      alcance_horizontal: Number((v0x * tiempo_vuelo).toFixed(4)),
      altura_maxima: Number((altura_inicial + Math.pow(v0y, 2) / (2 * GRAVEDAD)).toFixed(4))
    },
    message: "Simulación de Tiro Parabólico calculada exitosamente."
  };
}

export function simularMCU(radio: number, velocidad_angular: number, tiempo_total_simulacion: number, posicion_angular_inicial: number = 0, num_puntos: number = 100) {
  if (radio <= 0) throw new Error("El radio debe ser positivo");
  const estados_simulacion = [];
  const paso_tiempo = tiempo_total_simulacion / (num_puntos - 1);

  for (let i = 0; i < num_puntos; i++) {
    const t = i * paso_tiempo;
    const theta = posicion_angular_inicial + velocidad_angular * t;
    const x = radio * Math.cos(theta);
    const y = radio * Math.sin(theta);

    estados_simulacion.push({
      tiempo: Number(t.toFixed(4)),
      posicion_x: Number(x.toFixed(4)),
      posicion_y: Number(y.toFixed(4)),
      angulo: Number(theta.toFixed(4))
    });
  }

  return {
    parametros_entrada: { radio, velocidad_angular, tiempo_total_simulacion },
    resultados: {
      tiempo_total_simulacion,
      estados_simulacion
    },
    message: "Simulación de MCU calculada exitosamente."
  };
}

export function simularMAS(amplitud: number, frecuencia_angular: number, fase_inicial: number = 0, tiempo_total_simulacion: number, num_puntos: number = 100) {
  const estados_simulacion = [];
  const paso_tiempo = tiempo_total_simulacion / (num_puntos - 1);

  for (let i = 0; i < num_puntos; i++) {
    const t = i * paso_tiempo;
    const theta = frecuencia_angular * t + fase_inicial;
    const x = amplitud * Math.cos(theta);
    const v = -amplitud * frecuencia_angular * Math.sin(theta);
    const a = -amplitud * Math.pow(frecuencia_angular, 2) * Math.cos(theta);

    estados_simulacion.push({
      tiempo: Number(t.toFixed(4)),
      posicion: Number(x.toFixed(4)),
      velocidad: Number(v.toFixed(4)),
      aceleracion: Number(a.toFixed(4))
    });
  }

  return {
    parametros_entrada: { amplitud, frecuencia_angular, tiempo_total_simulacion },
    resultados: {
      tiempo_total_simulacion,
      estados_simulacion
    },
    message: "Simulación de MAS calculada exitosamente."
  };
}

export function simularPenduloSimple(longitud: number, angulo_inicial_grados: number, velocidad_angular_inicial: number = 0, tiempo_total_simulacion: number, num_puntos: number = 100) {
  const estados_simulacion = [];
  const paso_tiempo = tiempo_total_simulacion / (num_puntos - 1);
  const theta0 = angulo_inicial_grados * (Math.PI / 180);
  const omega0 = velocidad_angular_inicial;
  const w = Math.sqrt(GRAVEDAD / longitud); // natural frequency
  
  // Approximation for small angles: theta(t) = A*cos(w*t + phi)
  // A*cos(phi) = theta0
  // -A*w*sin(phi) = omega0
  const A = Math.sqrt(Math.pow(theta0, 2) + Math.pow(omega0 / w, 2));
  const phi = Math.atan2(-omega0 / w, theta0);

  for (let i = 0; i < num_puntos; i++) {
    const t = i * paso_tiempo;
    const theta = A * Math.cos(w * t + phi);
    const omega = -A * w * Math.sin(w * t + phi);
    const alpha = -A * Math.pow(w, 2) * Math.cos(w * t + phi);
    
    const x = longitud * Math.sin(theta);
    const y = -longitud * Math.cos(theta);

    estados_simulacion.push({
      tiempo: Number(t.toFixed(4)),
      posicion_angular: Number(theta.toFixed(4)),
      velocidad_angular: Number(omega.toFixed(4)),
      aceleracion_angular: Number(alpha.toFixed(4)),
      posicion_x: Number(x.toFixed(4)),
      posicion_y: Number(y.toFixed(4))
    });
  }

  return {
    parametros_entrada: { longitud, angulo_inicial_grados, tiempo_total_simulacion },
    resultados: {
      tiempo_total_simulacion,
      estados_simulacion
    },
    message: "Simulación de Péndulo Simple calculada exitosamente."
  };
}
