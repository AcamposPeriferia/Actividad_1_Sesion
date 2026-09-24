from app.container import account_repository


def transfer(client, from_account, to_account, amount):
    return client.post(
        "/transfers",
        json={"from_account": from_account, "to_account": to_account, "amount": amount},
    )


def test_transfer_successfully(client):
    response = transfer(client, "ACC-001", "ACC-002", 100_000.0)

    assert response.status_code == 200
    assert response.json() == {
        "message": "Transfer completed",
        "from_account": "ACC-001",
        "to_account": "ACC-002",
        "amount": 100_000.0,
    }
    assert account_repository.get_balance("ACC-001") == 3_400_000.0
    assert account_repository.get_balance("ACC-002") == 950_000.0


def test_transfer_fails_when_origin_account_does_not_exist(client):
    response = transfer(client, "UNKNOWN", "ACC-002", 100.0)

    assert response.status_code == 400
    assert response.json()["detail"] == "Origin account does not exist"


def test_transfer_fails_when_destination_account_does_not_exist(client):
    response = transfer(client, "ACC-001", "UNKNOWN", 100.0)

    assert response.status_code == 400
    assert response.json()["detail"] == "Destination account does not exist"


def test_transfer_fails_when_accounts_are_the_same(client):
    response = transfer(client, "ACC-001", "ACC-001", 100.0)

    assert response.status_code == 400
    assert response.json()["detail"] == "Origin and destination accounts must be different"


def test_transfer_fails_when_there_are_not_enough_funds(client):
    response = transfer(client, "ACC-002", "ACC-001", 900_000.0)

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"
    assert account_repository.get_balance("ACC-002") == 850_000.0


def test_transfer_fails_when_amount_is_not_positive(client):
    for amount in (0, -50.0):
        response = transfer(client, "ACC-001", "ACC-002", amount)

        assert response.status_code == 400
        assert response.json()["detail"] == "Monto invalido: debe ser mayor a 0"
    assert account_repository.get_balance("ACC-001") == 3_500_000.0


def test_completed_transfer_appears_in_history(client):
    transfer(client, "ACC-003", "ACC-004", 2_500_000.0)

    history = client.get("/transfers").json()

    assert len(history) == 1
    assert history[0]["transfer_id"] == "TRF-00001"
    assert history[0]["from_account"] == "ACC-003"
    assert history[0]["amount"] == 2_500_000.0


def test_rejected_transfer_is_not_in_history(client):
    transfer(client, "ACC-002", "ACC-001", 900_000.0)

    assert client.get("/transfers").json() == []
