'use client';

import Link from 'next/link';
import { useState, useEffect, use, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { gsap } from 'gsap';


// Definir interfaces para los datos de la simulación y los resultados
interface SimulationParams {
  // Ejemplo: masa_kg: number, velocidad_inicial_mps: number, etc.
  [key: string]: any;
}

interface SimulationResult {
  // Estructura de los resultados, puede variar por simulación
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
  estados_simulacion?: any[]; // Add this line for animation states
}

interface ChartDataPoint {
  tiempo: number;
  [key: string]: number;
}

interface SimulationData {
  tipo_simulacion: string;
  parametros_entrada: SimulationParams;
  resultados: SimulationResult;
  mensaje?: string; // Add optional message field
  error?: string; // Add optional error field
}

interface ParamDefinition {
  name: string;
  label: string;
  unit?: string;
}

interface SimulationPageProps {
  params: Promise<{
    slug: string;
  }>;
}

const getFormulasForSimulation = (simSlug: string): string[] => {
  switch (simSlug) {
    case 'caida-libre':
      return [
        'y = y₀ + v₀t - ½gt²',
        'v = v₀ - gt'
      ];
    case 'mru':
      return [
        'x = x₀ + vt'
      ];
    case 'mruv':
      return [
        'x = x₀ + v₀t + ½at²',
        'v = v₀ + at'
      ];
    case 'tiro-parabolico':
      return [
        'x = x₀ + v₀ₓt',
        'y = y₀ + v₀ᵧt - ½gt²'
      ];
    // Add other simulations as needed
    default:
      return [];
  }
};

const SimulationPage = ({ params }: SimulationPageProps) => {
  const { slug } = use(params);
  const [simulationData, setSimulationData] = useState<SimulationData | null>(null);
  // const [inputParams, setInputParams] = useState<SimulationParams>({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [graphData, setGraphData] = useState<ChartDataPoint[]>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const timelineRef = useRef<gsap.core.Timeline | null>(null);
  const circleRef = useRef<SVGCircleElement>(null);
  const timeTextRef = useRef<SVGTextElement>(null);
  const xAxisRef = useRef<SVGLineElement>(null);
  const yAxisRef = useRef<SVGLineElement>(null);
  const xAxisLabelRef = useRef<SVGTextElement>(null);
  const yAxisLabelRef = useRef<SVGTextElement>(null);
  const trajectoryPathRef = useRef<SVGPathElement>(null);

  const handlePlayPause = () => {
    if (timelineRef.current) {
      if (isPlaying) {
        timelineRef.current.pause();
      } else {
        timelineRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleReset = () => {
    if (timelineRef.current) {
      timelineRef.current.restart();
      timelineRef.current.pause();
      setIsPlaying(false);
    }
  };

  useEffect(() => {
    if (simulationData && shouldDisplayChart(slug)) {
      setGraphData(formatDataForChart(simulationData));
    }
  }, [simulationData, slug]);

  useEffect(() => {
    if (simulationData?.resultados?.estados_simulacion && simulationData.resultados.estados_simulacion.length > 0) {
      const estados = simulationData.resultados.estados_simulacion;
      console.log("Estados de simulación recibidos:", estados);

      if (!circleRef.current || !timeTextRef.current) return;

      // Calculate min/max values for scaling
      let minX = Infinity, maxX = -Infinity;
      let minY = Infinity, maxY = -Infinity;

      estados.forEach(estado => {
        switch (slug) {
          case 'mru':
          case 'mruv':
          case 'movimiento-armonico-simple':
            if (estado.posicion !== undefined) {
              minX = Math.min(minX, estado.posicion);
              maxX = Math.max(maxX, estado.posicion);
            }
            break;
          case 'caida-libre':
            if (estado.altura !== undefined) {
              minY = Math.min(minY, estado.altura);
              maxY = Math.max(maxY, estado.altura);
            }
            break;
          case 'tiro-parabolico':
            if (estado.posicion_x !== undefined) {
              minX = Math.min(minX, estado.posicion_x);
              maxX = Math.max(maxX, estado.posicion_x);
            }
            if (estado.posicion_y !== undefined) {
              minY = Math.min(minY, estado.posicion_y);
              maxY = Math.max(maxY, estado.posicion_y);
            }
            // Ensure minX and minY are at least 0 for parabolic motion
            minX = Math.min(minX, 0);
            minY = Math.min(minY, 0);
            break;
          case 'movimiento-circular-uniforme':
          case 'pendulo-simple':
            if (estado.posicion_x !== undefined) {
              minX = Math.min(minX, estado.posicion_x);
              maxX = Math.max(maxX, estado.posicion_x);
            }
            if (estado.posicion_y !== undefined) {
              minY = Math.min(minY, estado.posicion_y);
              maxY = Math.max(maxY, estado.posicion_y);
            }
            break;
        }
      });

      // Determine scaling factors and offsets
      const padding = 10; // Padding inside the 100x100 viewBox
      const viewBoxWidth = 100;
      const viewBoxHeight = 100;

      let scaleX = 1, offsetX = 0;
      let scaleY = 1, offsetY = 0;

      if (maxX !== -Infinity && minX !== Infinity && (maxX - minX) > 0) {
        scaleX = (viewBoxWidth - 2 * padding) / (maxX - minX);
        offsetX = padding - minX * scaleX;
      } else {
        // Default to center if no movement or single point
        offsetX = viewBoxWidth / 2 - (estados[0]?.posicion_x || estados[0]?.posicion || 0) * scaleX;
      }

      if (maxY !== -Infinity && minY !== Infinity && (maxY - minY) > 0) {
        scaleY = (viewBoxHeight - 2 * padding) / (maxY - minY);
        offsetY = padding - minY * scaleY; // Invert Y-axis for SVG
      } else {
        // Default to center if no movement or single point
        offsetY = viewBoxHeight / 2 - (estados[0]?.posicion_y || estados[0]?.altura || 0) * scaleY;
      }

      // Ensure initial state is set
      const initialEstado = estados[0];
      let initialCx = 50;
      let initialCy = 50;

      switch (slug) {
        case 'mru':
        case 'mruv':
        case 'movimiento-armonico-simple':
          initialCx = initialEstado.posicion !== undefined ? initialEstado.posicion * scaleX + offsetX : 50;
          initialCy = 50; // Y remains centered for 1D motion
          break;
        case 'caida-libre':
          initialCx = 50; // X remains centered for 1D motion
          initialCy = initialEstado.altura !== undefined ? viewBoxHeight - (initialEstado.altura * scaleY + offsetY) : 50; // Invert Y for display
          break;
        case 'tiro-parabolico':
        case 'movimiento-circular-uniforme':
        case 'pendulo-simple':
          initialCx = initialEstado.posicion_x !== undefined ? initialEstado.posicion_x * scaleX + offsetX : 50;
          initialCy = initialEstado.posicion_y !== undefined ? viewBoxHeight - (initialEstado.posicion_y * scaleY + offsetY) : 50; // Invert Y for display
          break;
      }
      gsap.set(circleRef.current, { attr: { cx: initialCx, cy: initialCy } });
      timeTextRef.current.textContent = `Tiempo: ${initialEstado.tiempo?.toFixed(2) || '0.00'} s`;

      // Create a GSAP timeline
      timelineRef.current = gsap.timeline({
        paused: true,
        onUpdate: () => {
          const currentTime = timelineRef.current?.time() || 0;
          // Find the closest state based on time
          let currentEstado = estados[0];
           let index = 0; // Initialize index outside the loop
           for (let i = 0; i < estados.length; i++) {
             if (estados[i].tiempo <= currentTime) {
               currentEstado = estados[i];
               index = i; // Update index
             } else {
               break;
             }
           }

          if (circleRef.current && timeTextRef.current) {
            // Update circle position based on simulation type and currentEstado
            switch (slug) {
              case 'mru':
              case 'mruv':
              case 'movimiento-armonico-simple':
                gsap.set(circleRef.current, { attr: { cx: currentEstado.posicion * scaleX + offsetX } });
                // Update X-axis label and Y-axis label visibility for 1D motion
                if (xAxisRef.current && yAxisRef.current && xAxisLabelRef.current && yAxisLabelRef.current) {
                  gsap.set(xAxisRef.current, { attr: { x1: 0, y1: 50, x2: 100, y2: 50 }, opacity: 1 });
                  gsap.set(yAxisRef.current, { opacity: 0 }); // Hide Y-axis for 1D motion
                  gsap.set(xAxisLabelRef.current, { text: 'Posición (m)', x: 98, y: 52, opacity: 1 });
                  gsap.set(yAxisLabelRef.current, { opacity: 0 }); // Hide Y-axis label
                }
                timeTextRef.current.textContent = `Tiempo: ${currentEstado.tiempo?.toFixed(2) || '0.00'} s\nPosición: ${currentEstado.posicion?.toFixed(2) || '0.00'} m`;
                if (slug === 'mruv') {
                  timeTextRef.current.textContent += `\nVelocidad: ${currentEstado.velocidad?.toFixed(2) || '0.00'} m/s\nAceleración: ${currentEstado.aceleracion?.toFixed(2) || '0.00'} m/s²`;
                }
                break;
              case 'caida-libre':
                gsap.set(circleRef.current, { attr: { cy: viewBoxHeight - (currentEstado.altura * scaleY + offsetY) } });
                // Update X-axis label and Y-axis label visibility for 1D motion
                if (xAxisRef.current && yAxisRef.current && xAxisLabelRef.current && yAxisLabelRef.current) {
                  gsap.set(xAxisRef.current, { opacity: 0 }); // Hide X-axis for 1D vertical motion
                  gsap.set(yAxisRef.current, { attr: { x1: 50, y1: 0, x2: 50, y2: 100 }, opacity: 1 });
                  gsap.set(xAxisLabelRef.current, { opacity: 0 }); // Hide X-axis label
                  gsap.set(yAxisLabelRef.current, { text: 'Altura (m)', x: 52, y: 5, opacity: 1 });
                }
                timeTextRef.current.textContent = `Tiempo: ${currentEstado.tiempo?.toFixed(2) || '0.00'} s\nAltura: ${currentEstado.altura?.toFixed(2) || '0.00'} m\nVelocidad: ${currentEstado.velocidad?.toFixed(2) || '0.00'} m/s`;
                break;
              case 'tiro-parabolico':
              case 'movimiento-circular-uniforme':
              case 'pendulo-simple':
              gsap.set(circleRef.current, { attr: { cx: currentEstado.posicion_x * scaleX + offsetX, cy: viewBoxHeight - (currentEstado.posicion_y * scaleY + offsetY) } });
              // Update X-axis label and Y-axis label visibility for 2D motion
              if (xAxisRef.current && yAxisRef.current && xAxisLabelRef.current && yAxisLabelRef.current) {
                gsap.set(xAxisRef.current, { attr: { x1: 0 * scaleX + offsetX, y1: viewBoxHeight - (0 * scaleY + offsetY), x2: 100, y2: viewBoxHeight - (0 * scaleY + offsetY) }, opacity: 1 });
                gsap.set(yAxisRef.current, { attr: { x1: 0 * scaleX + offsetX, y1: 0, x2: 0 * scaleX + offsetX, y2: 100 }, opacity: 1 });
                gsap.set(xAxisLabelRef.current, { text: 'X', x: 98, y: viewBoxHeight - (0 * scaleY + offsetY) + 2, opacity: 1 });
                gsap.set(yAxisLabelRef.current, { text: 'Y', x: (0 * scaleX + offsetX) - 2, y: 5, opacity: 1 });
              }
              timeTextRef.current.textContent = `Tiempo: ${currentEstado.tiempo?.toFixed(2) || '0.00'} s\nPosición X: ${currentEstado.posicion_x?.toFixed(2) || '0.00'} m\nPosición Y: ${currentEstado.posicion_y?.toFixed(2) || '0.00'} m\nVelocidad X: ${currentEstado.velocidad_x?.toFixed(2) || '0.00'} m/s\nVelocidad Y: ${currentEstado.velocidad_y?.toFixed(2) || '0.00'} m/s`;
              break;
          }
          timeTextRef.current.textContent = `Tiempo: ${currentEstado.tiempo?.toFixed(2) || '0.00'} s\n` +
            (currentEstado.posicion !== undefined ? `Posición: ${currentEstado.posicion?.toFixed(2) || '0.00'} m\n` : '') +
            (currentEstado.altura !== undefined ? `Altura: ${currentEstado.altura?.toFixed(2) || '0.00'} m\n` : '') +
            (currentEstado.posicion_x !== undefined ? `Posición X: ${currentEstado.posicion_x?.toFixed(2) || '0.00'} m\n` : '') +
            (currentEstado.posicion_y !== undefined ? `Posición Y: ${currentEstado.posicion_y?.toFixed(2) || '0.00'} m\n` : '') +
            (currentEstado.velocidad !== undefined ? `Velocidad: ${currentEstado.velocidad?.toFixed(2) || '0.00'} m/s\n` : '') +
            (currentEstado.velocidad_x !== undefined ? `Velocidad X: ${currentEstado.velocidad_x?.toFixed(2) || '0.00'} m/s\n` : '') +
            (currentEstado.velocidad_y !== undefined ? `Velocidad Y: ${currentEstado.velocidad_y?.toFixed(2) || '0.00'} m/s\n` : '') +
            (currentEstado.aceleracion !== undefined ? `Aceleración: ${currentEstado.aceleracion?.toFixed(2) || '0.00'} m/s²` : '');
          }
        },
        onComplete: () => {
          setIsPlaying(false);
        }
      });

      // Set up the animation for the circle
      const animationDuration = estados[estados.length - 1].tiempo;
      timelineRef.current?.to(circleRef.current, {
        duration: animationDuration,
        ease: 'none',
        motionPath: {
          path: estados.map(estado => {
            switch (slug) {
              case 'mru':
              case 'mruv':
                return { x: estado.posicion * scaleX + offsetX, y: 50 };
              case 'caida-libre':
                return { x: 50, y: viewBoxHeight - (estado.altura * scaleY + offsetY) };
              case 'tiro-parabolico':
              case 'movimiento-circular-uniforme':
              case 'pendulo-simple':
                return { x: estado.posicion_x * scaleX + offsetX, y: viewBoxHeight - (estado.posicion_y * scaleY + offsetY) };
              default:
                return { x: 50, y: 50 };
            }
          }),
          curviness: 0, // Straight line for linear motion
        },
      });

      // Draw trajectory path
      if (trajectoryPathRef.current) {
        const pathData = estados.map((estado, i) => {
          let x, y;
          switch (slug) {
            case 'mru':
            case 'mruv':
              x = estado.posicion * scaleX + offsetX;
              y = 50; // Keep Y constant for 1D motion
              break;
            case 'caida-libre':
              x = 50; // Keep X constant for 1D motion
              y = viewBoxHeight - (estado.altura * scaleY + offsetY);
              break;
            case 'tiro-parabolico':
            case 'movimiento-circular-uniforme':
            case 'pendulo-simple':
              x = estado.posicion_x * scaleX + offsetX;
              y = viewBoxHeight - (estado.posicion_y * scaleY + offsetY);
              break;
            default:
              x = 50;
              y = 50;
          }
          return `${i === 0 ? 'M' : 'L'}${x},${y}`;
        }).join(' ');
        gsap.set(trajectoryPathRef.current, { attr: { d: pathData } });
      }
    }

    return () => {
      if (timelineRef.current) {
        timelineRef.current.kill(); // Destroy the timeline on unmount or data change
      }
    };
  }, [simulationData, slug]);

  const togglePlayPause = () => {
    setIsPlaying(prev => !prev);
  };

  // const handleReset = () => {
  //   setIsPlaying(false);
  //   animationTimeline.current?.seek(0);
  // };

  const isChartableSimulation = (simSlug: string): boolean => {
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

  const formatChartData = (resultados: SimulationResult, simSlug: string): ChartDataPoint[] => {
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
            posicion_x: resultados.posiciones?.[i] || 0,
            velocidad_x: resultados.velocidades?.[i] || 0,
          }));
          break;
        case 'mruv':
          data = tiempos.map((t, i) => ({
            tiempo: t,
            posicion_x: resultados.posiciones?.[i] || 0,
            velocidad_x: resultados.velocidades?.[i] || 0,
            aceleracion_x: resultados.aceleraciones?.[i] || 0,
          }));
          break;
        case 'fuerzas-leyes-newton':
          data = tiempos.map((t, i) => ({
            tiempo: t,
            posicion_x: resultados.posiciones?.[i] || 0,
            velocidad_x: resultados.velocidades?.[i] || 0,
            aceleracion_x: resultados.aceleraciones?.[i] || 0,
            fuerza: resultados.fuerzas?.[i] || 0,
          }));
          break;
        case 'energia-potencial-conservacion':
          data = tiempos.map((t, i) => ({
            tiempo: t,
            posicion_y: resultados.posiciones?.[i] || 0,
            velocidad_y: resultados.velocidades?.[i] || 0,
            energia_potencial: resultados.energias_potenciales?.[i] || 0,
            energia_cinetica: resultados.energias_cineticas?.[i] || 0,
            energia_total: resultados.energias_totales?.[i] || 0,
          }));
          break;
        case 'energia-potencial-elastica':
          data = tiempos.map((t, i) => ({
            tiempo: t,
            posicion_x: resultados.posiciones?.[i] || 0,
            velocidad_x: resultados.velocidades?.[i] || 0,
            fuerza: resultados.fuerzas?.[i] || 0,
            energia_potencial: resultados.energias_potenciales?.[i] || 0,
            energia_cinetica: resultados.energias_cineticas?.[i] || 0,
            energia_total: resultados.energias_totales?.[i] || 0,
          }));
          break;
        case 'ondas-transversales':
          data = tiempos.map((t, i) => ({
            tiempo: t,
            posicion_x: resultados.posiciones_x?.[i] || 0,
            posicion_y: resultados.posiciones_y?.[i] || 0,
            amplitud: resultados.amplitudes?.[i] || 0,
          }));
          break;
        case 'ondas-longitudinales':
          data = tiempos.map((t, i) => ({
            tiempo: t,
            posicion_x: resultados.posiciones_x?.[i] || 0,
            posicion_y: resultados.posiciones_y?.[i] || 0,
            desplazamiento: resultados.desplazamientos?.[i] || 0,
          }));
          break;
        case 'circuitos-rc':
          data = tiempos.map((t, i) => ({
            tiempo: t,
            voltaje_capacitor: resultados.voltajes_capacitor?.[i] || 0,
            corriente: resultados.corrientes?.[i] || 0,
          }));
          break;
        case 'circuitos-rl':
          data = tiempos.map((t, i) => ({
            tiempo: t,
            voltaje_inductor: resultados.voltajes_inductor?.[i] || 0,
            corriente: resultados.corrientes?.[i] || 0,
          }));
          break;
        default:
          // Default to using 'tiempos' and 'posiciones' if available
          if (resultados.tiempos && resultados.posiciones) {
            data = resultados.tiempos.map((t, i) => ({
              tiempo: t,
              posicion: resultados.posiciones?.[i] || 0,
            }));
          }
          break;
      }
      return data;
    }
  };

  const getExpectedParamsForSimulation = (simSlug: string): ParamDefinition[] => {
    switch (simSlug) {
      case 'caida-libre':
        return [
          { name: 'altura_inicial', label: 'Altura Inicial', unit: 'm' },
        ];
      case 'tiro-parabolico':
        return [
          { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
          { name: 'angulo_lanzamiento_grados', label: 'Ángulo de Lanzamiento', unit: '°' },
          { name: 'altura_inicial', label: 'Altura Inicial', unit: 'm' },

        ];
      case 'plano-inclinado':
        return [
          { name: 'masa_kg', label: 'Masa', unit: 'kg' },
          { name: 'angulo_inclinacion_grados', label: 'Ángulo de Inclinación', unit: '°' },
          { name: 'longitud_plano_m', label: 'Longitud del Plano', unit: 'm' },
          { name: 'coeficiente_friccion', label: 'Coeficiente de Fricción' },
        ];
      case 'colision-elastica-1d':
        return [
          { name: 'masa1_kg', label: 'Masa 1', unit: 'kg' },
          { name: 'velocidad1_inicial_mps', label: 'Velocidad Inicial 1', unit: 'm/s' },
          { name: 'masa2_kg', label: 'Masa 2', unit: 'kg' },
          { name: 'velocidad2_inicial_mps', label: 'Velocidad Inicial 2', unit: 'm/s' },
        ];
      case 'colision-inelastica-1d':
        return [
          { name: 'masa1_kg', label: 'Masa 1', unit: 'kg' },
          { name: 'velocidad1_inicial_mps', label: 'Velocidad Inicial 1', unit: 'm/s' },
          { name: 'masa2_kg', label: 'Masa 2', unit: 'kg' },
          { name: 'velocidad2_inicial_mps', label: 'Velocidad Inicial 2', unit: 'm/s' },
        ];
      case 'movimiento-circular-uniforme':
        return [
          { name: 'radio_m', label: 'Radio', unit: 'm' },
          { name: 'velocidad_angular_rad_s', label: 'Velocidad Angular', unit: 'rad/s' },
          { name: 'velocidad_tangencial_mps', label: 'Velocidad Tangencial', unit: 'm/s' },
        ];
      case 'movimiento-armonico-simple':
        return [
          { name: 'amplitud_m', label: 'Amplitud', unit: 'm' },
          { name: 'frecuencia_angular_rad_s', label: 'Frecuencia Angular', unit: 'rad/s' },
          { name: 'fase_inicial_rad', label: 'Fase Inicial', unit: 'rad' },
        ];
      case 'pendulo-simple':
        return [
          { name: 'longitud_m', label: 'Longitud', unit: 'm' },
          { name: 'angulo_inicial_grados', label: 'Ángulo Inicial', unit: '°' },
        ];
      case 'colision-elastica-2d':
        return [
          { name: 'm1_kg', label: 'Masa 1', unit: 'kg' },
          { name: 'v1ix_mps', label: 'Velocidad Inicial 1 (X)', unit: 'm/s' },
          { name: 'v1iy_mps', label: 'Velocidad Inicial 1 (Y)', unit: 'm/s' },
          { name: 'm2_kg', label: 'Masa 2', unit: 'kg' },
          { name: 'v2ix_mps', label: 'Velocidad Inicial 2 (X)', unit: 'm/s' },
          { name: 'v2iy_mps', label: 'Velocidad Inicial 2 (Y)', unit: 'm/s' },
        ];
      case 'colision-inelastica-2d':
        return [
          { name: 'm1_kg', label: 'Masa 1', unit: 'kg' },
          { name: 'v1ix_mps', label: 'Velocidad Inicial 1 (X)', unit: 'm/s' },
          { name: 'v1iy_mps', label: 'Velocidad Inicial 1 (Y)', unit: 'm/s' },
          { name: 'm2_kg', label: 'Masa 2', unit: 'kg' },
          { name: 'v2ix_mps', label: 'Velocidad Inicial 2 (X)', unit: 'm/s' },
          { name: 'v2iy_mps', label: 'Velocidad Inicial 2 (Y)', unit: 'm/s' },
        ];
      case 'colision-elastica-3d':
        return [
          { name: 'm1_kg', label: 'Masa 1', unit: 'kg' },
          { name: 'v1_inicial_mps', label: 'Velocidad Inicial 1', unit: 'm/s' },
          { name: 'm2_kg', label: 'Masa 2', unit: 'kg' },
          { name: 'v2_inicial_mps', label: 'Velocidad Inicial 2', unit: 'm/s' },
        ];
      case 'colision-inelastica-3d':
        return [
          { name: 'm1_kg', label: 'Masa 1', unit: 'kg' },
          { name: 'v1_inicial_mps', label: 'Velocidad Inicial 1', unit: 'm/s' },
          { name: 'm2_kg', label: 'Masa 2', unit: 'kg' },
          { name: 'v2_inicial_mps', label: 'Velocidad Inicial 2', unit: 'm/s' },
        ];
      case 'mru': // Movimiento Rectilíneo Uniforme
        return [
          { name: 'posicion_inicial', label: 'Posición Inicial', unit: 'm'},
          { name: 'velocidad', label: 'Velocidad', unit: 'm/s' },
          { name: 'tiempo_total', label: 'Tiempo Total', unit: 's' },
        ];
      case 'mruv': // Movimiento Rectilíneo Uniformemente Variado
        return [
          { name: 'posicion_inicial', label: 'Posición Inicial', unit: 'm' },
          { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
          { name: 'aceleracion', label: 'Aceleración', unit: 'm/s²' },
          { name: 'tiempo_total_simulacion', label: 'Tiempo Total', unit: 's' },
        ];
      case 'fuerzas-leyes-newton':
        return [
          { name: 'masa_kg', label: 'Masa', unit: 'kg' },
          { name: 'fuerza_neta_N', label: 'Fuerza Neta', unit: 'N' },
          { name: 'tiempo_s', label: 'Tiempo', unit: 's' },
          { name: 'velocidad_inicial_mps', label: 'Velocidad Inicial', unit: 'm/s' },
          { name: 'posicion_inicial_m', label: 'Posición Inicial', unit: 'm' },
        ];
      case 'trabajo-energia':
        return [
          { name: 'masa', label: 'Masa', unit: 'kg' },
          { name: 'velocidad_inicial', label: 'Velocidad Inicial', unit: 'm/s' },
          { name: 'fuerza', label: 'Fuerza', unit: 'N' },
          { name: 'distancia', label: 'Distancia', unit: 'm' },
          { name: 'angulo', label: 'Ángulo', unit: '°' },
        ];
      case 'energia-potencial-gravitatoria':
        return [
          { name: 'masa', label: 'Masa', unit: 'kg' },
          { name: 'altura', label: 'Altura', unit: 'm' },
        ];
      case 'energia-potencial-elastica':
        return [
          { name: 'constante_elastica', label: 'Constante Elástica', unit: 'N/m' },
          { name: 'desplazamiento', label: 'Desplazamiento', unit: 'm' },
        ];
      case 'ley-ohm':
        return [
          { name: 'voltaje', label: 'Voltaje', unit: 'V' },
          { name: 'corriente', label: 'Corriente', unit: 'A' },
          { name: 'resistencia', label: 'Resistencia', unit: 'Ω' },
        ];
      case 'potencia-ohm':
        return [
          { name: 'voltaje', label: 'Voltaje', unit: 'V' },
          { name: 'corriente', label: 'Corriente', unit: 'A' },
          { name: 'resistencia', label: 'Resistencia', unit: 'Ω' },
        ];
      case 'resistencia-circuito':
        return [
          { name: 'resistencias', label: 'Resistencias (separadas por comas)', unit: 'Ω' },
          { name: 'tipo_circuito', label: 'Tipo de Circuito (serie/paralelo)' },
        ];
      case 'ley-kirchhoff-voltaje':
        return [
          { name: 'voltajes', label: 'Voltajes (separados por comas)', unit: 'V' },
        ];
      case 'ley-kirchhoff-corriente':
        return [
          { name: 'corrientes_entrantes', label: 'Corrientes Entrantes (separadas por comas)', unit: 'A' },
          { name: 'corrientes_salientes', label: 'Corrientes Salientes (separadas por comas)', unit: 'A' },
        ];
      case 'campo-magnetico':
        return [
          { name: 'corriente', label: 'Corriente', unit: 'A' },
          { name: 'distancia', label: 'Distancia', unit: 'm' },
        ];
      case 'fuerza-lorentz':
        return [
          { name: 'carga', label: 'Carga', unit: 'C' },
          { name: 'velocidad', label: 'Velocidad', unit: 'm/s' },
          { name: 'campo_magnetico', label: 'Campo Magnético', unit: 'T' },
          { name: 'angulo', label: 'Ángulo', unit: '°' },
        ];
      case 'flujo-magnetico':
        return [
          { name: 'campo_magnetico', label: 'Campo Magnético', unit: 'T' },
          { name: 'area', label: 'Área', unit: 'm²' },
          { name: 'angulo', label: 'Ángulo', unit: '°' },
        ];
      case 'ley-faraday':
        return [
          { name: 'cambio_flujo_magnetico', label: 'Cambio de Flujo Magnético', unit: 'Wb' },
          { name: 'cambio_tiempo', label: 'Cambio de Tiempo', unit: 's' },
        ];
      case 'capacitancia':
        return [
          { name: 'carga', label: 'Carga', unit: 'C' },
          { name: 'voltaje', label: 'Voltaje', unit: 'V' },
        ];
      case 'carga-voltaje-capacitor':
        return [
          { name: 'capacitancia', label: 'Capacitancia', unit: 'F' },
          { name: 'voltaje', label: 'Voltaje', unit: 'V' },
          { name: 'carga', label: 'Carga', unit: 'C' },
        ];
      case 'circuitos-serie-paralelo':
        return [
          { name: 'componentes', label: 'Valores de Componentes (separados por comas)' },
          { name: 'tipo', label: 'Tipo de Componente (resistencias/capacitores/inductores)' },
          { name: 'conexion', label: 'Tipo de Conexión (serie/paralelo)' },
        ];
      case 'corriente-voltaje-total':
        return [
          { name: 'corrientes', label: 'Corrientes (separadas por comas)', unit: 'A' },
          { name: 'voltajes', label: 'Voltajes (separadas por comas)', unit: 'V' },
          { name: 'tipo', label: 'Tipo (corriente/voltaje)' },
        ];
      case 'divisor-voltaje':
        return [
          { name: 'voltaje_total', label: 'Voltaje Total', unit: 'V' },
          { name: 'resistencias', label: 'Resistencias (separadas por comas)', unit: 'Ω' },
          { name: 'resistencia_objetivo', label: 'Resistencia Objetivo', unit: 'Ω' },
        ];
      case 'energia-potencia-electrica':
        return [
          { name: 'voltaje', label: 'Voltaje', unit: 'V' },
          { name: 'corriente', label: 'Corriente', unit: 'A' },
          { name: 'tiempo', label: 'Tiempo', unit: 's' },
        ];
      case 'caida-voltaje':
        return [
          { name: 'corriente', label: 'Corriente', unit: 'A' },
          { name: 'resistencia', label: 'Resistencia', unit: 'Ω' },
        ];
      case 'eficiencia-electrica':
        return [
          { name: 'potencia_salida', label: 'Potencia de Salida', unit: 'W' },
          { name: 'potencia_entrada', label: 'Potencia de Entrada', unit: 'W' },
        ];
      case 'inductancia':
        return [
          { name: 'flujo_magnetico', label: 'Flujo Magnético', unit: 'Wb' },
          { name: 'corriente', label: 'Corriente', unit: 'A' },
        ];
      case 'energia-inductor':
        return [
          { name: 'inductancia', label: 'Inductancia', unit: 'H' },
          { name: 'corriente', label: 'Corriente', unit: 'A' },
        ];
      case 'longitud-onda':
        return [
          { name: 'velocidad', label: 'Velocidad', unit: 'm/s' },
          { name: 'frecuencia', label: 'Frecuencia', unit: 'Hz' },
        ];
      case 'frecuencia-onda':
        return [
          { name: 'velocidad', label: 'Velocidad', unit: 'm/s' },
          { name: 'longitud_onda', label: 'Longitud de Onda', unit: 'm' },
        ];
      case 'velocidad-onda':
        return [
          { name: 'frecuencia', label: 'Frecuencia', unit: 'Hz' },
          { name: 'longitud_onda', label: 'Longitud de Onda', unit: 'm' },
        ];
      default:
        console.warn(`Parámetros no definidos para la simulación: ${simSlug}. Usando parámetros por defecto.`);
        return [
          { name: 'parametro_desconocido_1', label: 'Parámetro Desconocido 1' },
          { name: 'parametro_desconocido_2', label: 'Parámetro Desconocido 2' },
        ];
    }
  };

  const getOptionalParamsForSimulation = (simSlug: string): string[] => {
    switch (simSlug) {
      case 'tiro-parabolico':
        return ['altura_inicial'];
      case 'plano-inclinado':
        return ['coeficiente_friccion', 'masa_kg'];
      case 'ley-ohm':
      case 'potencia-ohm':
        return ['voltaje', 'corriente', 'resistencia']; // Permite 2 de 3
      case 'resistencia-circuito':
        return ['tipo_circuito'];
      case 'ley-kirchhoff-voltaje':
        return ['voltajes'];
      case 'ley-kirchhoff-corriente':
        return ['corrientes_entrantes', 'corrientes_salientes'];
      case 'campo-magnetico':
        return ['corriente', 'distancia'];
      case 'fuerza-lorentz':
        return ['angulo'];
      case 'flujo-magnetico':
        return ['angulo'];
      case 'carga-voltaje-capacitor':
        return ['voltaje', 'carga']; // Permite 2 de 3
      case 'circuitos-serie-paralelo':
        return ['tipo', 'conexion'];
      case 'corriente-voltaje-total':
        return ['tipo'];
      case 'divisor-voltaje':
        return ['resistencia_objetivo'];
      case 'energia-potencia-electrica':
        return ['tiempo'];
      case 'longitud-onda':
      case 'frecuencia-onda':
      case 'velocidad-onda':
        return ['velocidad', 'frecuencia', 'longitud_onda']; // Permite 2 de 3
      default:
        return [];
    }
  };

  const shouldDisplayChart = (simSlug: string): boolean => {
    // First check if it's a chartable simulation and has results
    if (!isChartableSimulation(simSlug) || !simulationData?.resultados) {
      return false;
    }

    // Then check if any of the required data arrays exist and have length > 0
    return (
      (simulationData.resultados.tiempos?.length ?? 0) > 0 ||
      (simulationData.resultados.posiciones?.length ?? 0) > 0 ||
      (simulationData.resultados.alturas?.length ?? 0) > 0 ||
      (simulationData.resultados.posiciones_x?.length ?? 0) > 0 ||
      (simulationData.resultados.posiciones_y?.length ?? 0) > 0 ||
      (simulationData.resultados.angulos?.length ?? 0) > 0 ||
      (simulationData.resultados.velocidades?.length ?? 0) > 0 ||
      (simulationData.resultados.aceleraciones?.length ?? 0) > 0 ||
      (simulationData.resultados.energias_potenciales?.length ?? 0) > 0 ||
      (simulationData.resultados.energias_cineticas?.length ?? 0) > 0 ||
      (simulationData.resultados.energias_totales?.length ?? 0) > 0 ||
      (simulationData.resultados.posiciones_angular?.length ?? 0) > 0 ||
      (simulationData.resultados.velocidades_angular?.length ?? 0) > 0 ||
      (simulationData.resultados.aceleraciones_angular?.length ?? 0) > 0 ||
      (simulationData.resultados.posiciones_x_cartesianas?.length ?? 0) > 0 ||
      (simulationData.resultados.posiciones_y_cartesianas?.length ?? 0) > 0 ||
      (simulationData.resultados.estados_simulacion?.length ?? 0) > 0
    );
  };

  const formatDataForChart = (data: SimulationData): any[] => {
    if (!data || !data.resultados || !Array.isArray(data.resultados)) {
      return [];
    }

    // Asumiendo que cada objeto en el array de resultados tiene una clave 'tiempo'
    // y otras claves numéricas para los valores a graficar.
    return data.resultados.map(item => {
      const formattedItem: any = { tiempo: item.tiempo };
      for (const key in item) {
        if (key !== 'tiempo' && typeof item[key] === 'number') {
          formattedItem[key] = item[key];
        }
      }
      return formattedItem;
    });
  };

  const chartData = simulationData ? formatDataForChart(simulationData) : [];

  const handleInputChange = (name: string, value: string) => {
    setInputParams(prev => {
      const paramDef = expectedParams.find(p => p.name === name);
      const parsedValue = value === '' ? undefined : parseFloat(value);
      return {
        ...prev,
        [name]: parsedValue,
      };
    });
  };

  const handleSimulate = async () => {
    setIsLoading(true);
    setError(null);
    setSimulationData(null);

    // Filtrar parámetros vacíos o indefinidos antes de enviar
    const paramsToSend: SimulationParams = {};
    for (const key in inputParams) {
      if (inputParams[key] !== '' && inputParams[key] !== undefined) {
        paramsToSend[key] = inputParams[key];
      }
    }

    try {
      const response = await fetch(`http://localhost:5000/simulacion/${slug}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(paramsToSend),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Error ${response.status} al realizar la simulación.`);
      }

      const data = await response.json();
      console.log("Datos recibidos del backend:", data); // Añadir este console.log
      setSimulationData(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Ocurrió un error al procesar la simulación.');
    } finally {
      setIsLoading(false);
    }
  };

  const expectedParams = getExpectedParamsForSimulation(slug);
  const [inputParams, setInputParams] = useState<SimulationParams>(() => {
    const initialParams: SimulationParams = {};
    expectedParams.forEach(param => {
      if ('defaultValue' in param && param.defaultValue !== undefined) {
        initialParams[param.name] = param.defaultValue;
      }
    });
    return initialParams;
  });

  const formulas = getFormulasForSimulation(slug);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2 bg-background text-foreground">
      <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
        <h1 className="text-4xl font-bold mb-6 text-primary">
          Simulación de {slug.replace(/-/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase())}
        </h1>

        {/* Input Parameters Section */}
        <div className="mb-8 w-full max-w-md">
          <h2 className="text-2xl font-bold mb-4 text-center text-gray-600 dark:text-gray-300">Parámetros de Entrada</h2>
          {expectedParams.map(param => (
            <div key={param.name} className="flex items-center mb-4">
              <label htmlFor={param.name} className="mr-4 text-muted-foreground w-1/2 text-right">
                {param.label} {param.unit && `(${param.unit})`}:
              </label>
              <Input
                id={param.name}
                type="number"
                value={inputParams[param.name] || ''}
                onChange={(e) => handleInputChange(param.name, e.target.value)}
                className="w-1/2 bg-card text-card-foreground border-border"
              />
            </div>
          ))}
          {/* Add optional parameters if needed */}
        </div>

        {/* Formulas Section */}
        {formulas.length > 0 && (
          <div className="mb-8 w-full max-w-md p-4 border rounded-lg shadow-md bg-card text-card-foreground">
            <h2 className="text-2xl font-bold mb-4 text-center text-gray-600 dark:text-gray-300">Fórmulas Utilizadas</h2>
            <ul className="list-disc list-inside text-left">
              {formulas.map((formula, index) => (
                <li key={index} className="mb-2 text-lg">
                  {formula}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Simulate Button */}
        <Button onClick={handleSimulate} disabled={isLoading} className="mb-8 bg-primary text-primary-foreground hover:bg-primary/90">
          {isLoading ? 'Simulando...' : 'Simular'}
        </Button>

        {/* Error Message */}
        {error && (
          <p className="text-destructive mb-4">Error: {error}</p>
        )}

        {/* Simulation Results Section */}
        {simulationData && (
          <div className="mt-8 w-full max-w-3xl text-left">
            <h2 className="text-2xl font-bold mb-4 text-center text-gray-600 dark:text-gray-300">Resultados</h2>
            
            {/* Animation Section */}
            {simulationData?.resultados?.estados_simulacion && simulationData.resultados.estados_simulacion.length > 0 ? (
              <div className="mt-8">
                <h2 className="text-2xl font-bold mb-4">Animación</h2>
                <div className="relative w-full h-[500px] bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                  <svg className="w-full h-full" viewBox="0 0 100 100">
                    {/* Initial circle position (will be updated by GSAP) */}
                    <circle ref={circleRef} cx="50" cy="50" r="5" fill="blue" />
                    {/* X-axis line */}
                    <line ref={xAxisRef} x1="0" y1="50" x2="100" y2="50" stroke="gray" strokeWidth="0.2" />
                    {/* Y-axis line */}
                    <line ref={yAxisRef} x1="50" y1="0" x2="50" y2="100" stroke="gray" strokeWidth="0.2" />
                    {/* X-axis label */}
                    <text ref={xAxisLabelRef} x="98" y="52" textAnchor="end" className="text-[0.3rem] fill-current text-gray-700 dark:text-gray-300">X</text>
                    {/* Y-axis label */}
                    <text ref={yAxisLabelRef} x="48" y="5" textAnchor="middle" className="text-[0.3rem] fill-current text-gray-700 dark:text-gray-300">Y</text>
                    {/* Trajectory Path */}
                    <path ref={trajectoryPathRef} fill="none" stroke="red" strokeWidth="0.5" strokeDasharray="1,1" />
                    {/* Display current time, position, velocity, and acceleration */}
                    <text ref={timeTextRef} x="50" y="95" textAnchor="middle" className="text-[0.3rem] fill-current text-gray-700 dark:text-gray-300">
                      Tiempo: 0.00 s
                      X: 0.00 m
                      Y: 0.00 m
                      Vx: 0.00 m/s
                      Vy: 0.00 m/s
                      Ax: 0.00 m/s²
                      Ay: 0.00 m/s²
                    </text>
                  </svg>
                </div>

                <div className="flex justify-center mt-4 space-x-4">
                  <Button onClick={handlePlayPause} className="bg-green-500 hover:bg-green-600 text-white">
                    {isPlaying ? 'Pausar' : 'Reproducir'}
                  </Button>
                  <Button onClick={handleReset} className="bg-red-500 hover:bg-red-600 text-white">
                    Reiniciar
                  </Button>
                </div>
              </div>
            ) : (
              <p className="text-center text-muted-foreground">No animation data available for this simulation.</p>
            )}
            {/* {shouldDisplayChart(slug) && chartData.length > 0 ? (
              <div className="w-full h-[400px] mt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={chartData}
                    margin={{
                      top: 5,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="tiempo" label={{ value: 'Tiempo (s)', position: 'insideBottom', offset: -5 }} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {Object.keys(chartData[0] || {}).filter(key => key !== 'tiempo').map((dataKey, index) => (
                      <Line
                        key={dataKey}
                        type="monotone"
                        dataKey={dataKey}
                        stroke={`hsl(${index * 60}, 70%, 50%)`}
                        activeDot={{ r: 8 }}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            ) : (
              Object.entries(simulationData.resultados).map(([key, value]) => (
                <p key={key} className="mb-2 text-foreground">
                  <strong className="text-primary">{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong> {JSON.stringify(value)}
                </p>
              ))
            )} */}

            {/* Formulas Section */}
            {getFormulasForSimulation(slug).length > 0 && (
              <div className="mt-6">
                <h2 className="text-2xl font-bold mb-4 text-center text-gray-600 dark:text-gray-300">Fórmulas Utilizadas</h2>
                <ul className="list-disc list-inside text-muted-foreground">
                  {getFormulasForSimulation(slug).map((formula, index) => (
                    <li key={index}>{formula}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Back Button */}
        <div className="mt-8">
          <Link href="/">
            <Button variant="outline" className="bg-card text-card-foreground border-border hover:bg-card/90">
              Volver a la lista de simulaciones
            </Button>
          </Link>
        </div>
      </main>

      {/* Footer */}
      <footer className="flex items-center justify-center w-full h-24 border-t border-border bg-card text-card-foreground">
        <a href="https://github.com/hrcamilo11" target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground transition-colors duration-200">
          <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 inline-block align-middle mr-2">
            <title>GitHub</title>
            <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.73.084-.73 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.49.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12z"/>
          </svg>
          hrcamilo11
        </a>
      </footer>
    </div>
  );
};

export default SimulationPage;
