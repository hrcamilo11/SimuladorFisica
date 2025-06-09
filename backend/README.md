# Backend (Python)

Este directorio contiene el código del backend de la aplicación, desarrollado en Python con Flask.

## Configuración y Ejecución

Para configurar y ejecutar el backend, sigue los siguientes pasos:

1.  Asegúrate de estar en el directorio `backend`:
    ```bash
    cd backend
    ```

2.  (Opcional pero recomendado) Crea un entorno virtual:
    ```bash
    python -m venv venv
    ```

3.  Activa el entorno virtual:
    -   Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  Instala las dependencias listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

5.  Ejecuta la aplicación Flask:
    ```bash
    python main.py
    ```

El servidor backend se iniciará y estará disponible para recibir solicitudes del frontend.