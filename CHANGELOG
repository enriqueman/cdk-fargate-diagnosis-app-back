# CHANGELOG - Pipeline End-to-End para Detección de Enfermedades

## [Versión 2.0] - Semana 2 (Versión Actual)

### 🆕 **NUEVAS FUNCIONALIDADES**

#### **Recolección y Preprocesamiento Automatizado**
- **Apache NiFi**: Implementación de ingesta automática y centralizada desde fuentes hospitalarias
- **MLFlow**: Sistema de registro completo para reproducibilidad y trazabilidad
- **SNOMED CT**: Normalización mediante ontologías médicas estándar
- **TensorFlow GANs**: Generación de datos sintéticos para enfermedades huérfanas

#### **Control de Versiones y Gestión de Datos**
- **DVC (Data Version Control)**: Versionado de datasets vinculados a experimentos
- **Estratificación avanzada**: División por clases y regiones demográficas
- **SMOTE**: Técnicas de resampling para balanceo de clases

#### **Orquestación y Escalabilidad**
- **Kubeflow Pipelines**: Orquestación automatizada de experimentos reproducibles
- **MLFlow Model Registry**: Versionado automático de modelos con metadatos completos

#### **Opciones de Despliegue Flexibles**
- **Despliegue Local**: 
  - Exportación a ONNX/TorchScript
  - Interfaz gráfica Python (PyQt/Tkinter)
  - Ejecución offline con ONNX Runtime/TensorFlow Lite
- **Despliegue en Nube**: Mantenido de v1.0 con mejoras

#### **Monitorización Avanzada**
- **Grafana**: Dashboards en tiempo real para métricas de inferencia
- **Prometheus/CloudWatch**: Recolección de métricas y detección de drift
- **Reentrenamiento Automatizado**: Activado por detección de drift >15%

### 🔄 **CAMBIOS PRINCIPALES**

#### **Arquitectura de Procesamiento**
- **ANTES (v1.0)**: Procesamiento manual y conversión básica NLP
- **AHORA (v2.0)**: Pipeline automatizado con Apache NiFi + MLFlow + DVC

#### **Gestión de Modelos**
- **ANTES (v1.0)**: Modelos estáticos con validación básica
- **AHORA (v2.0)**: Orquestación con Kubeflow + registro automático en MLFlow

#### **Flexibilidad de Despliegue**
- **ANTES (v1.0)**: Solo despliegue en nube (AWS)
- **AHORA (v2.0)**: Opción híbrida (local + nube) para diferentes contextos

#### **Monitorización**
- **ANTES (v1.0)**: QuickSight para visualización
- **AHORA (v2.0)**: Grafana + Prometheus para monitorización en tiempo real

### ✨ **MEJORAS TÉCNICAS**

#### **Reproducibilidad y Trazabilidad**
- Integración completa MLFlow para seguimiento de experimentos
- DVC para versionado de datasets
- Kubeflow para pipelines reproducibles

#### **Calidad de Datos**
- Normalización con ontologías médicas estándar (SNOMED CT)
- Generación sintética mejorada con GANs en TensorFlow
- Estratificación demográfica avanzada

#### **Escalabilidad Operacional**
- Reentrenamiento automático basado en drift detection
- Sistema de flagging mejorado para retroalimentación activa
- Múltiples opciones de despliegue según necesidades

---

## [Versión 1.0] - Semana 1 (Versión Inicial)

### **Características Originales**
- Pipeline básico end-to-end
- Arquitectura híbrida (Random Forest + XGBoost para comunes, Few-shot learning para huérfanas)
- Despliegue exclusivo en AWS (ECS Fargate)
- Frontend Next.js + Backend FastAPI
- Monitorización con QuickSight
- Validación clínica con pruebas A/B

---

## **Resumen de Impacto de Cambios**

| **Aspecto** | **v1.0** | **v2.0** | **Impacto** |
|-------------|----------|----------|-------------|
| **Automatización** | Manual | Apache NiFi + MLFlow | 🚀 **Alto** |
| **Reproducibilidad** | Básica | MLFlow + DVC + Kubeflow | 🚀 **Alto** |
| **Flexibilidad** | Solo nube | Híbrido (local + nube) | 🚀 **Alto** |
| **Monitorización** | QuickSight | Grafana + Prometheus | 🔧 **Medio** |
| **Escalabilidad** | Manual | Automatizada | 🚀 **Alto** |

### **Motivaciones del Cambio**
1. **Escalabilidad Operacional**: Automatización completa del pipeline
2. **Reproducibilidad Científica**: Trazabilidad total de experimentos y datos
3. **Flexibilidad de Despliegue**: Adaptación a diferentes contextos hospitalarios
4. **Calidad de Datos**: Normalización estándar y generación sintética mejorada
5. **Mantenibilidad**: Sistemas de monitorización y reentrenamiento automático

---

## **Repositorios**

- **Frontend**: [enriqueman/cdk-fargate-diagnosis-app-nextjs](https://github.com/enriqueman/cdk-fargate-diagnosis-app-nextjs)
- **Backend**: [enriqueman/cdk-fargate-diagnosis-app-back](https://github.com/enriqueman/cdk-fargate-diagnosis-app-back)

---

**Autor**: Enrique Manzano  
**Última actualización**: Semana 2