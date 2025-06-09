// src/app/page.tsx
'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

interface Simulation {
  nombre: string;
  descripcion: string;
  endpoint: string;
}

interface SimulationsData {
  simulaciones_disponibles: Simulation[];
}

async function getSimulations(): Promise<SimulationsData> {
  // Asegúrate de que el backend esté corriendo en localhost:5001
  const res = await fetch('http://localhost:5001/');
  if (!res.ok) {
    // Esto activará el Error Boundary más cercano
    throw new Error('Failed to fetch simulations');
  }
  return res.json();
}

export default function Home() {
  const [simulations, setSimulations] = useState<Simulation[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getSimulations()
      .then(data => {
        setSimulations(data.simulaciones_disponibles);
      })
      .catch(err => {
        console.error(err);
        setError('No se pudo cargar la lista de simulaciones. Asegúrate de que el servidor backend esté en ejecución en http://localhost:5001.');
      });
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground py-8 px-4 sm:px-6 lg:px-8 font-[family-name:var(--font-geist-sans)]">
      <header className="text-center mb-12">
        <h1 className="text-4xl font-bold">Simulador de Física Interactivo</h1>
        <p className="mt-2 text-lg">Explora diversos fenómenos físicos mediante simulaciones interactivas.</p>
      </header>

      <main className="max-w-4xl mx-auto">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6" role="alert">
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <h2 className="text-2xl font-semibold mb-6">Simulaciones Disponibles:</h2>
        
        {simulations.length > 0 ? (
          <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {simulations.map((sim, index) => (
              <li key={sim.endpoint || sim.nombre || index} className="bg-card text-card-foreground shadow-lg rounded-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 ease-in-out">
                <Link href={`/simulacion${sim.endpoint ? sim.endpoint.replace('/simulacion', '') : ''}`} className="block p-6">
                  <h3 className="text-xl font-semibold text-primary hover:text-primary-foreground mb-2">{sim.nombre}</h3>
                  <p className="text-muted-foreground text-sm">{sim.descripcion}</p>
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          !error && <p className="text-muted-foreground">Cargando simulaciones...</p>
        )}
      </main>

      <footer className="text-center mt-12 py-6 border-t border-border">
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
}
