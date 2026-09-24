def test_list_accounts_returns_seed_data(client):
    response = client.get("/accounts")

    assert response.status_code == 200
    accounts = {a["account_id"]: a for a in response.json()}
    assert set(accounts) == {"ACC-001", "ACC-002", "ACC-003", "ACC-004"}
    assert accounts["ACC-003"]["account_type"] == "CORPORATIVA"


def test_get_account(client):
    response = client.get("/accounts/ACC-001")

    assert response.status_code == 200
    assert response.json() == {
        "account_id": "ACC-001",
        "owner": "Laura Gómez",
        "account_type": "PERSONAL",
        "balance": 3_500_000.0,
    }


def test_get_account_not_found(client):
    response = client.get("/accounts/UNKNOWN")

    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"
