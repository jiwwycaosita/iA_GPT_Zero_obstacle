"""Tests simples pour vérifier que l'API répond localement."""

import requests

API_BASE_URL = "http://localhost:8080"


def test_health():
    response = requests.get(f"{API_BASE_URL}/health", timeout=10)
    print("HEALTH:", response.status_code, response.text)


def test_general():
    orchestration_request = {
        "task": "general",
        "text": "Explique-moi en étapes simples comment fonctionne un formulaire d'aide financière (en général).",
    }
    response = requests.post(
        f"{API_BASE_URL}/agent/orchestrate", json=orchestration_request, timeout=60
    )
    print("GENERAL:", response.status_code, response.text[:500])


if __name__ == "__main__":
    test_health()
    print("-----")
    test_general()
