def test_completed_transfer_is_audited(client):
    client.post(
        "/transfers",
        json={"from_account": "ACC-001", "to_account": "ACC-002", "amount": 50_000.0},
    )

    events = client.get("/audit-events").json()

    assert len(events) == 1
    assert events[0]["event_type"] == "TRANSFER_COMPLETED"
    assert events[0]["details"]["transfer_id"] == "TRF-00001"
    assert events[0]["details"]["amount"] == 50_000.0


def test_rejected_transfer_is_audited_with_reason(client):
    client.post(
        "/transfers",
        json={"from_account": "ACC-001", "to_account": "ACC-002", "amount": -1},
    )

    events = client.get("/audit-events").json()

    assert len(events) == 1
    assert events[0]["event_type"] == "TRANSFER_REJECTED"
    assert events[0]["details"]["reason"] == "Monto invalido: debe ser mayor a 0"
