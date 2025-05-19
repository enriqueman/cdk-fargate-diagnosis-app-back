import pytest
from fastapi.testclient import TestClient
from app.main import app, STATS_FILE, PREDICTION_LOG 
import json
import os

@pytest.fixture
def client(tmp_path):
    # Configurar archivos temporales
    stats_file = tmp_path / "stats.json"
    log_file = tmp_path / "prediction_log.txt"
    
    # Monkey patching de las rutas de archivo
    from app.main import STATS_FILE, PREDICTION_LOG
    STATS_FILE = str(stats_file)
    PREDICTION_LOG = str(log_file)
    
    # Inicializar archivo de estadísticas
    with open(stats_file, 'w') as f:
        json.dump({
            "category_counts": {
                "NO ENFERMO": 0,
                "ENFERMEDAD LEVE": 0,
                "ENFERMEDAD AGUDA": 0,
                "ENFERMEDAD CRÓNICA": 0,
                "ENFERMEDAD TERMINAL": 0
            },
            "last_predictions": [],
            "last_date": None
        }, f)
    
    # Crear archivo de log vacío
    open(log_file, 'a').close()
    
    with TestClient(app) as client:
        yield client

def test_initial_stats(client):
    response = client.get("/api/report")
    assert response.status_code == 200
    data = response.json()
    assert data["category_counts"] == {
        "NO ENFERMO": 0,
        "ENFERMEDAD LEVE": 0,
        "ENFERMEDAD AGUDA": 0,
        "ENFERMEDAD CRÓNICA": 0,
        "ENFERMEDAD TERMINAL": 0
    }

def test_no_enfermo_diagnosis(client):
    payload = {
  "datos_personales": {
    "patientId": "string",
    "patientName": "string",
    "age": 0,
    "sex": "string",
    "weight": 0,
    "height": 0
  },
  "habitos": {
    "smoking": True,
    "alcohol": True,
    "drugs": True
  },
  "sintomas_principales": [
    {
      "nombre": "string",
      "severidad": 1
    }
  ],
  "sintomas_secundarios": {
    "fever": True,
    "rash": True,
    "cough": True,
    "skinEruptions": True,
    "nightSweats": True,
    "bloodInUrine": True,
    "bloodInStool": True,
    "constipation": False,
    "nausea": False,
    "headache": False,
    "abdominalPain": False,
    "insomnia": False,
    "fatigue": True,
    "diarrhea": False,
    "additionalSymptoms": ""
  }
}
    
    response = client.post("/api/diagnosis", json=payload)
    assert response.status_code == 200
    assert response.json()["diagnosis"] == "ENFERMEDAD AGUDA"
    
    # Verificar estadísticas
    report = client.get("/api/report").json()
    assert report["category_counts"]["ENFERMEDAD AGUDA"] == 1

def test_critical_symptoms_escalation(client):
    payload = {
        "datos_personales": {
        "patientId": "string",
        "patientName": "string",
        "age": 0,
        "sex": "string",
        "weight": 0,
        "height": 0
    },
    "habitos": {
        "smoking": False,
        "alcohol": False,
        "drugs": False
    },
    "sintomas_principales": [
        {
        "nombre": "string",
        "severidad": 1
        }
    ],
    "sintomas_secundarios": {
        "fever": False,
        "rash": False,
        "cough": False,
        "skinEruptions": False,
        "nightSweats": False,
        "bloodInUrine": False,
        "bloodInStool": False,
        "constipation": False,
        "nausea": False,
        "headache": False,
        "abdominalPain": False,
        "insomnia": False,
        "fatigue": False,
        "diarrhea": False,
        "additionalSymptoms": ""
    }
    }
    
    response = client.post("/api/diagnosis", json=payload)
    assert response.status_code == 200
    assert response.json()["diagnosis"] == "NO ENFERMO"

def test_all_categories(client):
    # Test para verificar las 5 categorías
    test_cases = [
        ({"severidad": 1, "sintomas": 0}, "NO ENFERMO"),
        ({"severidad": 3, "sintomas": 5}, "ENFERMEDAD LEVE"),
        ({"severidad": 4, "sintomas": 8}, "ENFERMEDAD AGUDA"),
        ({"severidad": 5, "sintomas": 10}, "ENFERMEDAD CRÓNICA"),
        ({"severidad": 5, "sintomas": 15}, "ENFERMEDAD TERMINAL")
    ]
    
    sintomas_keys = [
        "fever", "rash", "cough", "skinEruptions", "nightSweats",
        "bloodInUrine", "bloodInStool", "constipation", "nausea",
        "headache", "abdominalPain", "insomnia", "fatigue", "diarrhea"
    ]

    for case in test_cases:
        num_sintomas = case[0]["sintomas"]
        payload = {
            "datos_personales": {
                "patientId": "3",
                "patientName": "Test Case",
                "age": 40,
                "sex": "M",
                "weight": 80,
                "height": 180
            },
            "habitos": {
                "smoking": True,
                "alcohol": True,
                "drugs": True
            },
            "sintomas_principales": [
                {"nombre": "Síntoma", "severidad": case[0]["severidad"]}
            ],
            "sintomas_secundarios": {
                **{k: True for k in sintomas_keys[:num_sintomas]},
                **{k: False for k in sintomas_keys[num_sintomas:]},
                "additionalSymptoms": ""
            }
        }
        
        response = client.post("/api/diagnosis", json=payload)
        assert response.status_code == 200
        assert response.json()["diagnosis"] == case[1]