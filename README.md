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
   ```bash
   cd backend
   ```
2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   ```
3. Activa el entorno virtual:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Instala las dependencias (se especificarán en `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
5. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

### Frontend (Next.js)

1. Navega al directorio `frontend`:
   ```bash
   cd frontend
   ```
2. Instala las dependencias:
   ```bash
   npm install
   # o
   yarn install
   ```
3. Ejecuta la aplicación de desarrollo:
   ```bash
   npm run dev
   # o
   yarn dev
   ```

## Ejecutar Ambos Componentes

Para iniciar tanto el backend como el frontend simultáneamente, puedes usar el script `start_all.bat` (solo para Windows):

```bash
start_all.bat
```

## Casos de Simulación a Implementar

- Caída Libre
- Tiro Parabólico
- Planos Inclinados
- Colisiones (elásticas e inelásticas)
- Otros (a definir)

Cada simulación permitirá:
- Ingresar valores iniciales.
- Mostrar las fórmulas físicas aplicadas.
- Visualizar la simulación con animaciones.