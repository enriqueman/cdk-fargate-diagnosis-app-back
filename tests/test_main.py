import pytest
from fastapi.testclient import TestClient
from app.main import app
import json
import os

@pytest.fixture
def client(tmp_path):
    # Configurar archivos temporales
    stats_file = tmp_path / "stats.json"
    log_file = tmp_path / "prediction_log.txt"
    
    # Monkey patching de las rutas de archivo
    from main import STATS_FILE, PREDICTION_LOG
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
            "patientId": "1",
            "patientName": "Test Patient",
            "age": 25,
            "sex": "M",
            "weight": 70,
            "height": 175
        },
        "habitos": {
            "smoking": False,
            "alcohol": False,
            "drugs": False
        },
        "sintomas_principales": [{"nombre": "Tos leve", "severidad": 1}],
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
    
    # Verificar estadísticas
    report = client.get("/api/report").json()
    assert report["category_counts"]["NO ENFERMO"] == 1

def test_critical_symptoms_escalation(client):
    payload = {
        "datos_personales": {
            "patientId": "2",
            "patientName": "Critical Patient",
            "age": 30,
            "sex": "F",
            "weight": 60,
            "height": 165
        },
        "habitos": {
            "smoking": False,
            "alcohol": False,
            "drugs": False
        },
        "sintomas_principales": [{"nombre": "Fatiga", "severidad": 1}],
        "sintomas_secundarios": {
            "fever": True,
            "bloodInUrine": True,
            # Otros síntomas en False
            "rash": False,
            "cough": False,
            "skinEruptions": False,
            "nightSweats": False,
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
    assert response.json()["diagnosis"] == "ENFERMEDAD LEVE"

def test_all_categories(client):
    # Test para verificar las 5 categorías
    test_cases = [
        ({"severidad": 1, "sintomas": 0}, "NO ENFERMO"),
        ({"severidad": 3, "sintomas": 5}, "ENFERMEDAD LEVE"),
        ({"severidad": 4, "sintomas": 8}, "ENFERMEDAD AGUDA"),
        ({"severidad": 5, "sintomas": 10}, "ENFERMEDAD CRÓNICA"),
        ({"severidad": 5, "sintomas": 15}, "ENFERMEDAD TERMINAL")
    ]
    
    for case in test_cases:
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
                "fever": False,
                # Configurar síntomas según el caso
                **{k: True for k in list(app.schema()["components"]["schemas"]["SintomasSecundariosModel"]["properties"].keys())[:case[0]["sintomas"]]}
            }
        }
        
        response = client.post("/api/diagnosis", json=payload)
        assert response.status_code == 200
        assert response.json()["diagnosis"] == case[1]