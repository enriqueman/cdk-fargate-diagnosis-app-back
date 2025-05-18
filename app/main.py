from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Union
import random
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
import os

app = FastAPI(
    title="API de Diagnóstico Médico",
    description="API para diagnóstico de enfermedades basado en síntomas",
    version="1.0.0",
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, limitar a los orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos para almacenar estadísticas
STATS_FILE = "stats.json"
PREDICTION_LOG = "prediction_log.txt"

# Inicializar archivo de estadísticas si no existe
if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, "w") as f:
        initial_stats = {
            "category_counts": {
                "NO ENFERMO": 0,
                "ENFERMEDAD LEVE": 0,
                "ENFERMEDAD AGUDA": 0,
                "ENFERMEDAD CRÓNICA": 0,
                "ENFERMEDAD TERMINAL": 0
            },
            "last_predictions": [],
            "last_date": None
        }
        json.dump(initial_stats, f)

def update_prediction_stats(diagnosis: str):
    # Actualizar estadísticas
    with open(STATS_FILE, "r+") as f:
        stats = json.load(f)
        
        # Actualizar conteos
        stats["category_counts"][diagnosis] += 1
        
        # Actualizar últimas predicciones
        stats["last_predictions"].append({
            "diagnosis": diagnosis,
            "timestamp": datetime.now().isoformat()
        })
        # Mantener solo las últimas 5
        stats["last_predictions"] = stats["last_predictions"][-5:]
        
        # Actualizar última fecha
        stats["last_date"] = datetime.now().isoformat()
        
        # Guardar cambios
        f.seek(0)
        json.dump(stats, f)
        f.truncate()

def log_prediction(request_data: dict, diagnosis: str):
    # Registrar predicción en archivo de texto
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "patient_id": request_data.datos_personales.patientId,
        "patient_name": request_data.datos_personales.patientName,
        "age": request_data.datos_personales.age,
        "diagnosis": diagnosis,
        "symptoms": [s.nombre for s in request_data.sintomas_principales],
        "risk_factors": {
            "smoking": request_data.habitos.smoking,
            "alcohol": request_data.habitos.alcohol,
            "drugs": request_data.habitos.drugs
        }
    }
    
    with open(PREDICTION_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")




class HabitosModel(BaseModel):
    smoking: bool = False
    alcohol: bool = False
    drugs: bool = False

class SintomaBasicoModel(BaseModel):
    nombre: str
    severidad: int = 1  # 1-5

class SintomasSecundariosModel(BaseModel):
    fever: bool = False
    rash: bool = False
    cough: bool = False
    skinEruptions: bool = False
    nightSweats: bool = False
    bloodInUrine: bool = False
    bloodInStool: bool = False
    constipation: bool = False
    nausea: bool = False
    headache: bool = False
    abdominalPain: bool = False
    insomnia: bool = False
    fatigue: bool = False
    diarrhea: bool = False
    additionalSymptoms: str = ""

class DatosPersonalesModel(BaseModel):
    patientId: str
    patientName: str
    age: int
    sex: str
    weight: float
    height: float

class DiagnosisRequestModel(BaseModel):
    datos_personales: DatosPersonalesModel
    habitos: HabitosModel
    sintomas_principales: List[SintomaBasicoModel]
    sintomas_secundarios: SintomasSecundariosModel

class DiagnosisResponseModel(BaseModel):
    patientId: str
    patientName: str
    edad: int
    sexo: str
    diagnosis: str
    recomendaciones: str
    severidad: int
    riesgo: str

@app.get("/")
def read_root():
    return {"mensaje": "API de Diagnóstico Médico - Bienvenido"}

@app.post("/api/diagnosis", response_model=DiagnosisResponseModel)
def predict_diagnosis(request: DiagnosisRequestModel):
    try:
        # Calculamos la severidad basada en los síntomas principales
        primary_severity = sum([s.severidad for s in request.sintomas_principales])
        
        # Calculamos factores de riesgo
        risk_factors = 0
        if request.habitos.smoking:
            risk_factors += 1
        if request.habitos.alcohol:
            risk_factors += 1
        if request.habitos.drugs:
            risk_factors += 1
            
        # Contamos síntomas secundarios
        symptom_count = 0
        secundarios = request.sintomas_secundarios
        
        if secundarios.fever: symptom_count += 1
        if secundarios.rash: symptom_count += 1
        if secundarios.cough: symptom_count += 1
        if secundarios.skinEruptions: symptom_count += 1
        if secundarios.nightSweats: symptom_count += 1
        if secundarios.bloodInUrine: symptom_count += 1
        if secundarios.bloodInStool: symptom_count += 1
        if secundarios.constipation: symptom_count += 1
        if secundarios.nausea: symptom_count += 1
        if secundarios.headache: symptom_count += 1
        if secundarios.abdominalPain: symptom_count += 1
        if secundarios.insomnia: symptom_count += 1
        if secundarios.fatigue: symptom_count += 1
        if secundarios.diarrhea: symptom_count += 1
        
        # Calcula puntuación total de riesgo
        total_risk_score = primary_severity + risk_factors + min(10, symptom_count)
        
        # Determinamos el diagnóstico basado en la puntuación total
        if total_risk_score <= 6:
            diagnosis = "NO ENFERMO"
            recomendaciones = "No se requiere tratamiento en este momento. Descanso y buena alimentación."
            severidad = 0
            riesgo = "Bajo"
        elif total_risk_score <= 12:
            diagnosis = "ENFERMEDAD LEVE"
            recomendaciones = "Reposo, hidratación y medicamentos para síntomas específicos."
            severidad = 1
            riesgo = "Medio-Bajo"
        elif total_risk_score <= 18:
            diagnosis = "ENFERMEDAD AGUDA"
            recomendaciones = "Requiere atención médica inmediata. Posible tratamiento con antibióticos."
            severidad = 2
            riesgo = "Medio-Alto"
        elif total_risk_score <= 24:
            diagnosis = "ENFERMEDAD CRÓNICA"
            recomendaciones = "Requiere atención médica especializada y seguimiento continuo."
            severidad = 3
            riesgo = "Alto"
        else:
            diagnosis = "ENFERMEDAD TERMINAL"
            recomendaciones = "Cuidados paliativos y atención especializada requerida."
            severidad = 4
            riesgo = "Muy Alto"
        
        # Verificamos síntomas críticos que podrían elevar inmediatamente el diagnóstico
        if (secundarios.bloodInUrine or secundarios.bloodInStool) and secundarios.fever:
            # Presencia de sangre y fiebre siempre es preocupante
            if diagnosis == "NO ENFERMO":
                diagnosis = "ENFERMEDAD LEVE"
                recomendaciones = "Reposo, hidratación y medicamentos para síntomas específicos."
                severidad = 1
                riesgo = "Medio-Bajo"
            elif diagnosis == "ENFERMEDAD LEVE":
                diagnosis = "ENFERMEDAD AGUDA"
                recomendaciones = "Requiere atención médica inmediata. Posible tratamiento con antibióticos."
                severidad = 2
                riesgo = "Medio-Alto"
        
        update_prediction_stats(diagnosis)
        log_prediction(request, diagnosis)

        # Generamos respuesta
        return DiagnosisResponseModel(
            patientId=request.datos_personales.patientId,
            patientName=request.datos_personales.patientName,
            edad=request.datos_personales.age,
            sexo=request.datos_personales.sex,
            diagnosis=diagnosis,
            recomendaciones=recomendaciones,
            severidad=severidad,
            riesgo=riesgo
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento del diagnóstico: {str(e)}")

@app.post("/api/simplified-diagnosis")
def simplified_diagnosis(request: dict):
    """
    Endpoint simplificado para compatibilidad con la interfaz actual
    """
    try:
        # Extraer factores de riesgo 
        risk_factors = 0
        if request.get("smoking", False):
            risk_factors += 1
        if request.get("alcohol", False):
            risk_factors += 1
        if request.get("drugs", False):
            risk_factors += 1

        # Calcular severidad de síntomas primarios
        primary_severity = (
            int(request.get("severityLevel1", 1)) +
            int(request.get("severityLevel2", 1)) +
            int(request.get("severityLevel3", 1))
        )
            
        # Contar síntomas
        symptom_count = 0
        for symptom in ['fever', 'rash', 'cough', 'skinEruptions', 'nightSweats', 
                        'bloodInUrine', 'bloodInStool', 'constipation', 'nausea',
                        'headache', 'abdominalPain', 'insomnia', 'fatigue', 'diarrhea']:
            if request.get(symptom, False):
                symptom_count += 1
        
        # Sumar síntomas principales (si están rellenos)
        if request.get("primarySymptom", "").strip():
            symptom_count += 1
        if request.get("secondarySymptom", "").strip():
            symptom_count += 1
        if request.get("tertiarySymptom", "").strip():
            symptom_count += 1
        
        # Calcular puntuación total
        total_risk_score = primary_severity + risk_factors + min(10, symptom_count)
        
        # Determinar diagnóstico
        if total_risk_score <= 6:
            diagnosis = "NO ENFERMO"
        elif total_risk_score <= 12:
            diagnosis = "ENFERMEDAD LEVE"
        elif total_risk_score <= 18:
            diagnosis = "ENFERMEDAD AGUDA"
        elif total_risk_score <= 24:
            diagnosis = "ENFERMEDAD CRÓNICA"
        else:
            diagnosis = "ENFERMEDAD TERMINAL"
        
        # Verificar síntomas críticos 
        if (request.get("bloodInUrine", False) or request.get("bloodInStool", False)) and request.get("fever", False):
            if diagnosis == "NO ENFERMO":
                diagnosis = "ENFERMEDAD LEVE"
            elif diagnosis == "ENFERMEDAD LEVE":
                diagnosis = "ENFERMEDAD AGUDA"
        
        # Nuevo: Actualizar estadísticas
        with open(STATS_FILE, "r+") as f:
            stats = json.load(f)
            stats["category_counts"][diagnosis] += 1
            stats["last_predictions"].append({
                "diagnosis": diagnosis,
                "timestamp": datetime.now().isoformat()
            })
            stats["last_predictions"] = stats["last_predictions"][-5:]
            stats["last_date"] = datetime.now().isoformat()
            f.seek(0)
            json.dump(stats, f)
            f.truncate()
        return {
            "diagnosis": diagnosis,
            "riskScore": total_risk_score,
            "patientId": request.get("patientId", ""),
            "patientName": request.get("patientName", "")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el diagnóstico simplificado: {str(e)}")


# Nuevo endpoint para reportes
@app.get("/api/report")
def get_report():
    try:
        # Leer estadísticas
        with open(STATS_FILE, "r") as f:
            stats = json.load(f)
        
        # Leer últimas predicciones del log
        last_predictions = []
        if os.path.exists(PREDICTION_LOG):
            with open(PREDICTION_LOG, "r") as f:
                lines = f.readlines()[-5:]  # Últimas 5 líneas
                last_predictions = [json.loads(line) for line in lines]
        
        return {
            "category_counts": stats["category_counts"],
            "last_predictions": last_predictions,
            "last_prediction_date": stats["last_date"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Para ejecutar: uvicorn src.api.medical_diagnosis_api:app --reload