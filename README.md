# Modelo de Predicción Médica

Este repositorio contiene una solución para la predicción de diagnósticos médicos basada en síntomas del paciente. La aplicación está compuesta por un backend (API) y un frontend (interfaz web).

## Implementación Local

Para implementar la aplicación de forma local, es necesario desplegar tanto el backend como el frontend en ese orden.

### 1. Despliegue del Backend (API)

#### Construcción de la imagen Docker

1. Ubíquese en la carpeta raíz del proyecto:
   ```bash
   cd cdk-fargate-deploy-python-fastapi
   ```

2. Construya la imagen Docker:
   ```bash
   docker build -t myimage .
   ```

#### Ejecución del contenedor

1. Inicie el contenedor:
   ```bash
   docker run -d --name mycontainer -p 80:80 myimage
   ```

2. Una vez en ejecución, puede acceder a la documentación de la API en:
   ```
   http://127.0.0.1/docs
   ```
   Aquí encontrará todos los endpoints disponibles.

### 2. Despliegue del Frontend (Interfaz Web)

#### Construcción de la imagen Docker

1. Construya la imagen Docker del frontend:
   ```bash
   docker build --build-arg NEXT_PUBLIC_API_URL=http://127.0.0.1 -t nextjs-app .
   ```

#### Ejecución del contenedor

1. Inicie el contenedor:
   ```bash
   docker run -p 8080:80 nextjs-app
   ```

2. Acceda a la interfaz web en:
   ```
   http://localhost:8080
   ```

## Uso de la Aplicación

### Interfaz Local

1. Abra la aplicación en su navegador: `http://localhost:8080`
2. Complete el formulario con la información del paciente:
   - Llene la información básica requerida
   - Ingrese al menos 5 síntomas
3. Haga clic en el botón "Generar Predicción" en la parte inferior
4. Visualice los resultados de la predicción en el panel izquierdo

## Versión en Línea

Si dispone de conexión a internet, puede acceder a la versión desplegada de la aplicación:

### Frontend (Interfaz Web)
- URL: [https://pwa5h9m5vf.execute-api.us-east-1.amazonaws.com/](https://pwa5h9m5vf.execute-api.us-east-1.amazonaws.com/)
- Uso: Complete el formulario como se indica en las instrucciones locales

### Backend (API)
- Documentación de la API: [https://g6ag2ls1c7.execute-api.us-east-1.amazonaws.com/docs#](https://g6ag2ls1c7.execute-api.us-east-1.amazonaws.com/docs#)