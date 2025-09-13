from fastapi.testclient import TestClient

from payment_gateway_api.app import app
from payment_gateway_api.enums.payment_status import PaymentStatus


def test_request_with_valid_card_is_authorised():
    client = TestClient(app)
    response = client.post(
        "/payment", 
        json={
            "cardNumber": "1111111111111111",
            "expiryMonth": 12,
            "expiryYear": 2025,
            "currency": "USD",
            "amount": 10,
            "cvv": 123
        }
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert response_json["status"] == PaymentStatus.AUTHORIZED
    assert response_json["cardNumberLastFour"] == 1111
    assert response_json["expiryMonth"] == 12
    assert response_json["expiryYear"] == 2025
    assert response_json["currency"] == "USD"
    assert response_json["amount"] == 10


def test_request_with_invalid_card_is_rejected():
    client = TestClient(app)
    response = client.post(
        "/payment", 
        json={
            "cardNumber": "2222222222222222",
            "expiryMonth": 12,
            "expiryYear": 2025,
            "currency": "GBP",
            "amount": 10,
            "cvv": 123
        }
    )

    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert response_json["status"] == PaymentStatus.REJECTED
    assert response_json["cardNumberLastFour"] == 2222
    assert response_json["expiryMonth"] == 12
    assert response_json["expiryYear"] == 2025
    assert response_json["currency"] == "GBP"
    assert response_json["amount"] == 10
