// frontend/src/app/simulacion/[slug]/page.tsx
'use client';

import Link from 'next/link';
import { useState, use } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';


// Definir interfaces para los datos de la simulación y los resultados
interface SimulationParams {
  // Ejemplo: masa_kg: number, velocidad_inicial_mps: number, etc.
  [key: string]: any;
}

interface SimulationResult {
  // Estructura de los resultados, puede variar por simulación
  [key: string]: any;
}

interface SimulationData {
  tipo_simulacion: string;
  parametros_entrada: SimulationParams;
  formulas: string[];
  resultados: SimulationResult;
  // Otros campos que pueda devolver tu API
}

interface ParamDefinition {
  name: string;
  label: string;
  unit?: string;
}

interface SimulationPageProps {
  params: {
    slug: string;
  };
}

const SimulationPage = ({ params }: SimulationPageProps) => {
  //@ts-ignore
  const { slug } = use(params);
  const [simulationData, setSimulationData] = useState<SimulationData | null>(null);
  const [inputParams, setInputParams] = useState<SimulationParams>({});
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const getExpectedParamsForSimulation = (simSlug: string): ParamDefinition[] => {
    const timeDependentSimsDefault: ParamDefinition[] = [{ name: 'tiempo_total_s', label: 'Tiempo Total', unit: 's' }];
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
          ...timeDependentSimsDefault,
        ];
      case 'movimiento-armonico-simple':
        return [
          { name: 'amplitud_m', label: 'Amplitud', unit: 'm' },
          { name: 'frecuencia_angular_rad_s', label: 'Frecuencia Angular', unit: 'rad/s' },
          { name: 'fase_inicial_rad', label: 'Fase Inicial', unit: 'rad' },
          { name: 'tiempo_total_s', label: 'Tiempo Total', unit: 's' },
        ];
      case 'pendulo-simple':
        return [
          { name: 'longitud_m', label: 'Longitud', unit: 'm' },
          { name: 'angulo_inicial_grados', label: 'Ángulo Inicial', unit: '°' },
          { name: 'tiempo_total_s', label: 'Tiempo Total', unit: 's' },
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
          { name: 'posicion_inicial_m', label: 'Posición Inicial', unit: 'm' },
          { name: 'velocidad_mps', label: 'Velocidad', unit: 'm/s' },
          { name: 'tiempo_total_s', label: 'Tiempo Total', unit: 's' },
        ];
      case 'mruv': // Movimiento Rectilíneo Uniformemente Variado
        return [
          { name: 'posicion_inicial_m', label: 'Posición Inicial', unit: 'm' },
          { name: 'velocidad_inicial_mps', label: 'Velocidad Inicial', unit: 'm/s' },
          { name: 'aceleracion_mps2', label: 'Aceleración', unit: 'm/s²' },
          { name: 'tiempo_total_s', label: 'Tiempo Total', unit: 's' },
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
          { name: 'masa_kg', label: 'Masa', unit: 'kg' },
          { name: 'fuerza_N', label: 'Fuerza', unit: 'N' },
          { name: 'distancia_m', label: 'Distancia', unit: 'm' },
          { name: 'velocidad_inicial_mps', label: 'Velocidad Inicial', unit: 'm/s' },
          { name: 'angulo_fuerza_desplazamiento_grados', label: 'Ángulo Fuerza-Desplazamiento', unit: '°' },
        ];
      case 'energia-potencial-conservacion':
        return [
          { name: 'masa_kg', label: 'Masa', unit: 'kg' },
          { name: 'altura_inicial_m', label: 'Altura Inicial', unit: 'm' },
          { name: 'velocidad_inicial_y_mps', label: 'Velocidad Inicial Y', unit: 'm/s' },
        ];
      case 'energia-potencial-elastica':
        return [
          { name: 'masa_kg', label: 'Masa', unit: 'kg' },
          { name: 'constante_elastica_Npm', label: 'Constante Elástica', unit: 'N/m' },
          { name: 'amplitud_m', label: 'Amplitud', unit: 'm' },
          { name: 'tiempo_total_s', label: 'Tiempo Total', unit: 's' },
          { name: 'fase_inicial_grados', label: 'Fase Inicial', unit: '°' },
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
       default:
         return [];
     }
   };



  const handleInputChange = (name: string, value: string) => {
     setInputParams(prev => ({
       ...prev,
       [name]: value === '' ? undefined : parseFloat(value),
     }));
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
       const response = await fetch(`http://localhost:5001/simulacion/${slug}`,
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
      setSimulationData(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Ocurrió un error al procesar la simulación.');
    } finally {
      setIsLoading(false);
    }
  };

  const expectedParams = getExpectedParamsForSimulation(slug);

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
          <div className="mt-8 w-full max-w-md text-left">
            <h2 className="text-2xl font-bold mb-4 text-center text-gray-600 dark:text-gray-300">Resultados</h2>
            {Object.entries(simulationData.resultados).map(([key, value]) => (
              <p key={key} className="mb-2 text-foreground">
                <strong className="text-primary">{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong> {JSON.stringify(value)}
              </p>
            ))}

            {/* Formulas Section */}
            {simulationData.formulas && simulationData.formulas.length > 0 && (
              <div className="mt-6">
                <h2 className="text-2xl font-bold mb-4 text-center text-gray-600 dark:text-gray-300">Fórmulas Utilizadas</h2>
                <ul className="list-disc list-inside text-muted-foreground">
                  {simulationData.formulas.map((formula, index) => (
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