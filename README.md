# Chat de Usuario a Usuario con FastAPI y WebSockets

Implementa un servidor de chat en tiempo real para conversaciones de usuario a usuario en la aplicacion RentAll. Utiliza Python con el framework FastAPI y el protocolo WebSocket para una comunicación bidireccional eficiente.

## Características

-   **Chat en Tiempo Real**: Comunicación instantánea entre clientes conectados.
-   **Gestión de Conexiones**: El servidor gestiona activamente qué usuarios están conectados.
-   **Manejo de Zonas Horarias**: Los timestamps de los mensajes se generan en UTC en el servidor para garantizar la consistencia.
-   **Logging**: El servidor genera un archivo de log por cada sesión, registrando conexiones, desconexiones y mensajes enviados.

## Requisitos

-   Python 3.9+
-   Un gestor de paquetes como `pip`

## Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/Phanesan/rent-all-chat-service.git
    cd rent-all-chat-service
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # En Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

Para iniciar el servidor, ejecuta el siguiente comando en la raíz del proyecto:

```bash
uvicorn main:app --reload
```
