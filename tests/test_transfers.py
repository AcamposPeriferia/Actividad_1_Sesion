from fastapi.testclient import TestClient

from app.api.transfers import repository
from app.main import app

client = TestClient(app)


def reset_accounts():
    repository._accounts = {
        "ACC-001": 1000.0,
        "ACC-002": 500.0,
        "ACC-003": 200.0,
    }


def setup_function():
    reset_accounts()


def test_transfer_successfully():
    response = client.post(
        "/transfers",
        json={
            "from_account": "ACC-001",
            "to_account": "ACC-002",
            "amount": 100.0,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Transfer completed"
    assert repository.get_balance("ACC-001") == 900.0
    assert repository.get_balance("ACC-002") == 600.0


def test_transfer_fails_when_origin_account_does_not_exist():
    response = client.post(
        "/transfers",
        json={
            "from_account": "UNKNOWN",
            "to_account": "ACC-002",
            "amount": 100.0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Origin account does not exist"


def test_transfer_fails_when_there_are_not_enough_funds():
    response = client.post(
        "/transfers",
        json={
            "from_account": "ACC-003",
            "to_account": "ACC-002",
            "amount": 500.0,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"


def test_transfer_fails_when_amount_is_not_positive():
    for amount in (0, -50.0):
        response = client.post(
            "/transfers",
            json={
                "from_account": "ACC-001",
                "to_account": "ACC-002",
                "amount": amount,
            },
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Monto invalido: debe ser mayor a 0"
    assert repository.get_balance("ACC-001") == 1000.0
