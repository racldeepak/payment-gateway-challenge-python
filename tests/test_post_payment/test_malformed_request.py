from datetime import date
from typing import Dict, Union

from fastapi.testclient import TestClient

from payment_gateway_api.app import app


def get_sample_valid_payment_request() -> Dict[str, Union[str, int]]:
    today = date.today()
    return {
        "cardNumber": "0123456789012345",
        "expiryMonth": 12,
        "expiryYear": today.year + 1,
        "currency": "USD",
        "amount": 10,
        "cvv": 123
    }


def test_request_with_invalid_card_number_returns_400() -> None:
    client = TestClient(app)
    payment_request = get_sample_valid_payment_request()

    invalid_card_numbers = [
        None,
        "abcdefghijklmnop",
        "1234567890a12345",
        "1234",
        "1234567890123",
        "12345678901234567890"
    ]

    for card_number in invalid_card_numbers:
        payment_request["cardNumber"] = card_number
        response = client.post("/payment", json=payment_request)
        assert response.status_code == 400
        assert response.json()["message"] == "Rejected: Invalid payment request"


def test_request_with_invalid_expiry_month_returns_400() -> None:
    client = TestClient(app)
    payment_request = get_sample_valid_payment_request()

    invalid_expiry_months = [None, "1234", -1, 0, 13]

    for expiry_month in invalid_expiry_months:
        payment_request["expiryMonth"] = expiry_month
        response = client.post("/payment", json=payment_request)
        assert response.status_code == 400
        assert response.json()["message"] == "Rejected: Invalid payment request"


def test_request_with_invalid_expiry_year_returns_400() -> None:
    client = TestClient(app)
    payment_request = get_sample_valid_payment_request()

    invalid_expiry_years = [None, "1234", 2024, 2032]

    for expiry_year in invalid_expiry_years:
        payment_request["expiryYear"] = expiry_year
        response = client.post("/payment", json=payment_request)
        assert response.status_code == 400
        assert response.json()["message"] == "Rejected: Invalid payment request"


def test_request_with_invalid_currency_returns_400() -> None:
    client = TestClient(app)
    payment_request = get_sample_valid_payment_request()

    invalid_currencies = [None, "INVALID", 123]

    for currency in invalid_currencies:
        payment_request["currency"] = currency
        response = client.post("/payment", json=payment_request)
        assert response.status_code == 400
        assert response.json()["message"] == "Rejected: Invalid payment request"


def test_request_with_invalid_amount_returns_400() -> None:
    client = TestClient(app)
    payment_request = get_sample_valid_payment_request()

    invalid_amounts = [None, "INVALID", -1, 0]

    for amount in invalid_amounts:
        payment_request["amount"] = amount
        response = client.post("/payment", json=payment_request)
        assert response.status_code == 400
        assert response.json()["message"] == "Rejected: Invalid payment request"


def test_request_with_invalid_cvv_returns_400() -> None:
    client = TestClient(app)
    payment_request = get_sample_valid_payment_request()

    invalid_cvvs = [None, "12a", 12, 12345]

    for cvv in invalid_cvvs:
        payment_request["cvv"] = cvv
        response = client.post("/payment", json=payment_request)
        assert response.status_code == 400
        assert response.json()["message"] == "Rejected: Invalid payment request"


def test_request_with_expiry_date_in_past_returns_400() -> None:
    client = TestClient(app)
    payment_request = get_sample_valid_payment_request()
    
    today = date.today()
    invalid_expiry_dates = [
        (today.month, today.year - 1),
        (today.month - 1, today.year),
    ]

    for expiry_month, expiry_year in invalid_expiry_dates:
        payment_request["expiryMonth"] = expiry_month
        payment_request["expiryYear"] = expiry_year
        response = client.post("/payment", json=payment_request)
        assert response.status_code == 400
        assert response.json()["message"] == "Rejected: Invalid payment request"
