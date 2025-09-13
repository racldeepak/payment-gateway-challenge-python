from uuid import uuid4

from fastapi.testclient import TestClient

from payment_gateway_api.app import app
from payment_gateway_api.enums.payment_status import PaymentStatus
from payment_gateway_api.model.payment_details import PaymentDetails
from payment_gateway_api.repository.payments_repository import PaymentsRepository


def test_when_payment_with_id_exist_then_correct_payment_is_returned():
    paymentsRepository = PaymentsRepository()
    payment = PaymentDetails(
        id=uuid4(),
        status=PaymentStatus.AUTHORIZED,
        cardNumberLastFour=4321,
        expiryMonth=12,
        expiryYear=2024,
        currency="USD",
        amount=10
    )
    paymentsRepository.add(payment)
    
    client = TestClient(app)
    response = client.get("/payment/" + str(payment.id))

    assert response.status_code == 200
    assert response.json() == {
        "id": str(payment.id),
        "status": payment.status,
        "cardNumberLastFour": payment.cardNumberLastFour,
        "expiryMonth": payment.expiryMonth,
        "expiryYear": payment.expiryYear,
        "currency": payment.currency,
        "amount": payment.amount
    }


def test_when_payment_with_id_does_not_exist_then_404_is_returned():
    client = TestClient(app)
    response = client.get("/payment/" + str(uuid4()))

    assert response.status_code == 404
    assert response.json() == {
        "message": "Page not found"
    }
