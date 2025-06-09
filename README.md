# Simulador de Física Mecánica

Este proyecto tiene como objetivo crear un simulador interactivo para la clase de física mecánica, permitiendo a los usuarios simular diversos escenarios como caída libre, tiro parabólico, planos inclinados y colisiones.

## Estructura del Proyecto

El proyecto se dividirá en dos componentes principales:

- **Backend (Python):** Encargado de la lógica de las simulaciones, cálculos físicos y provisión de una API para el frontend.
- **Frontend (Next.js):** Responsable de la interfaz de usuario, visualización de las simulaciones y animaciones.

```
. (root)
├── backend/
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

Cada simulación permite:

-   Ingresar parámetros iniciales.
-   Visualizar las fórmulas físicas aplicadas.
-   Obtener resultados detallados de la simulación.