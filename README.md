# Simulador de Física Mecánica

Este proyecto tiene como objetivo crear un simulador interactivo para la clase de física mecánica, permitiendo a los usuarios simular diversos escenarios como caída libre, tiro parabólico, planos inclinados y colisiones.

## Estructura del Proyecto

El proyecto se dividirá en dos componentes principales:

- **Backend (Python):** Encargado de la lógica de las simulaciones, cálculos físicos y provisión de una API para el frontend.
- **Frontend (Next.js):** Responsable de la interfaz de usuario, visualización de las simulaciones y animaciones.

```
. (root)
├── backend/
│   ├── Ecuaciones/
│   ├── Formulas/
│   └── simulations/
└── frontend/
```

## Configuración Inicial

### Backend (Python)

1. Navega al directorio `backend`:
   Para instrucciones detalladas sobre cómo configurar y ejecutar cada componente, consulta los archivos `README.md` dentro de los directorios `backend/` y `frontend/` respectivamente.

## Ejecutar Ambos Componentes

Para iniciar tanto el backend como el frontend simultáneamente, puedes usar el script `start_all.bat` (solo para Windows):

```bash
start_all.bat
```

## Simulaciones Disponibles

El simulador incluye las siguientes simulaciones físicas:

-   Caída Libre
-   Tiro Parabólico
-   Movimiento Rectilíneo Uniforme (MRU)
-   Movimiento Rectilíneo Uniformemente Variado (MRUV)
-   Colisión Elástica 1D, 2D y 3D
-   Colisión Inelástica 1D, 2D y 3D
-   Péndulo Simple
-   Trabajo y Energía Cinética
-   Energía Potencial Gravitatoria y Conservación de Energía Mecánica
-   Energía Potencial Elástica y Conservación (Sistema Masa-Resorte)
-   Fuerzas y Leyes de Newton (2da Ley)
-   Plano Inclinado con Polea (en desarrollo)

Cada simulación permite:

-   Ingresar parámetros iniciales.
-   Visualizar las fórmulas físicas aplicadas.
-   Obtener resultados detallados de la simulación.

## Verificación de Funcionalidades

Para verificar que las funcionalidades actuales están operativas, sigue estos pasos:

1.  Asegúrate de que tanto el backend como el frontend estén corriendo. Puedes usar `start_all.bat`.
2.  Navega a la simulación específica en el frontend (ej. `http://localhost:3001/simulacion/plano-inclinado-polea`).
3.  Ingresa los parámetros requeridos y haz clic en el botón de simular.
4.  Abre la consola del navegador (F12) y verifica los logs para:
    -   `Raw simulation data from backend:`: Para confirmar que los datos se reciben del backend.
    -   `Simulation data after setting state:`: Para ver el estado de los datos de simulación en el frontend.
    -   `isChartableSimulation:`: Para verificar si la simulación es chartable.
    -   `Formatted chart data:`: Para ver los datos formateados para la gráfica/animación.
    -   Logs de `useEffect` y `onUpdate` para la animación: Para depurar el movimiento de los elementos SVG (`mass1Ref`, `mass2Ref`).