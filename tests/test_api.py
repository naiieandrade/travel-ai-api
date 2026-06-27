from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
HEADERS = {"X-API-Key": "travel-api-key"}


def test_classify_profile_success():
    response = client.post(
        "/api/v1/travel-profile/classify",
        headers=HEADERS,
        json={
            "preferencias": ["trilhas", "cachoeiras", "rapel"],
            "ritmo": "intenso",
            "orcamento": "medio",
            "companhia": "amigos"
        }
    )
    assert response.status_code == 200
    assert response.json()["perfil_detectado"] == "aventura"


def test_generate_itinerary_success():
    response = client.post(
        "/api/v1/itinerary/generate",
        headers=HEADERS,
        json={
            "destino": "Chapada dos Veadeiros",
            "dias": 2,
            "perfil": "aventura",
            "orcamento": "medio",
            "preferencias": ["trilhas", "cachoeiras"],
            "ritmo": "intenso"
        }
    )
    assert response.status_code == 200
    assert len(response.json()["roteiro"]) == 2


def test_validate_itinerary_success():
    response = client.post(
        "/api/v1/itinerary/validate",
        headers=HEADERS,
        json={
            "destino": "Rio de Janeiro",
            "dias": 1,
            "perfil": "relaxamento",
            "ritmo": "leve",
            "atividades": ["Trilha Pedra da Gávea", "Cristo Redentor", "Pão de Açúcar", "Museu do Amanhã"]
        }
    )
    assert response.status_code == 200
    assert response.json()["viavel"] is False


def test_missing_api_key():
    response = client.post(
        "/api/v1/travel-profile/classify",
        json={
            "preferencias": ["museu"],
            "ritmo": "leve",
            "orcamento": "baixo",
            "companhia": "solo"
        }
    )
    assert response.status_code == 401


def test_invalid_payload():
    response = client.post(
        "/api/v1/itinerary/generate",
        headers=HEADERS,
        json={
            "destino": "RJ",
            "dias": 0,
            "perfil": "aventura",
            "orcamento": "medio",
            "preferencias": [],
            "ritmo": "intenso"
        }
    )
    assert response.status_code == 422
