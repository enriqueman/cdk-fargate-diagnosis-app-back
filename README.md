# Sistema Predictivo para Detección de Enfermedades

## Problema

El diagnóstico oportuno de enfermedades, tanto comunes como huérfanas (raras), presenta desafíos considerables para los profesionales médicos debido a:

- Desbalance extremo en la disponibilidad de datos (miles de casos para enfermedades comunes vs. decenas para huérfanas)
- Variabilidad geográfica de síntomas según factores demográficos y ambientales
- Inconsistencias en la terminología médica y datos faltantes en registros clínicos
- Necesidad de alta precisión y baja latencia para entornos clínicos críticos

## Propósito

Este repositorio implementa un pipeline end-to-end para la detección de enfermedades comunes y huérfanas mediante modelos predictivos avanzados, con el objetivo de:

- Facilitar el diagnóstico médico con predicciones rápidas y explicables
- Mejorar los índices de salud pública a través de detección temprana
- Ofrecer un sistema que cumpla con normativas éticas y regulatorias de datos médicos
- Proporcionar una solución escalable y adaptable a diferentes entornos clínicos

## Estructura del Repositorio

.
├── app/
│   └── main.py                  # Función principal con el modelo predictivo
├── cdk_fargate_deploy/
│   └── cdk_fargate_deploy_stack.py  # Infraestructura para despliegue en AWS
├── app.py                       # Configuración del stack CDK
├── Dockerfile                   # Definición para construcción de imagen Docker
├── docker-compose.yml           # Composición de servicios Docker
└── requirements.txt             # Dependencias del proyecto


### Componentes Principales

- **main.py**: Contiene la implementación del modelo predictivo híbrido:
  - Modelo para enfermedades comunes (ensamblaje Random Forest + XGBoost)
  - Modelo para enfermedades huérfanas (Few-shot learning con Transformers)
  - Lógica de preprocesamiento de datos y predicción

- **cdk_fargate_deploy_stack.py**: Define la infraestructura como código para AWS:
  - Configuración de servicios ECS Fargate
  - Implementación de API Gateway
  - Configuración de bases de datos y almacenamiento
  - Mecanismos de seguridad y monitoreo

- **app.py**: Inicializa y configura el stack CDK para despliegue

- **Dockerfile** y **docker-compose.yml**: Permiten la construcción y orquestación de la imagen Docker para entornos de desarrollo y producción

## Despliegue

El sistema está diseñado para desplegarse en AWS utilizando:
- Frontend: Next.js en S3 (repositorio separado)
- Backend: API REST (FastAPI) en ECS Fargate
- Almacenamiento: PostgreSQL (RDS) y DynamoDB

## Repositorios Relacionados

- Frontend: [enriqueman/cdk-fargate-diagnosis-app-nextjs](https://github.com/enriqueman/cdk-fargate-diagnosis-app-nextjs)
- Backend: [enriqueman/cdk-fargate-diagnosis-app-back](https://github.com/enriqueman/cdk-fargate-diagnosis-app-back)


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