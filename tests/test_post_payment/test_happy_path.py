from fastapi.testclient import TestClient

from payment_gateway_api.app import app
from payment_gateway_api.enums.payment_status import PaymentStatus


def test_valid_payment_request_is_processed():
    client = TestClient(app)
    response = client.post(
        "/payment", 
        json={
            "cardNumber": "0123456789012345",
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
    assert response_json["cardNumberLastFour"] == 2345
    assert response_json["expiryMonth"] == 12
    assert response_json["expiryYear"] == 2025
    assert response_json["currency"] == "USD"
    assert response_json["amount"] == 10
