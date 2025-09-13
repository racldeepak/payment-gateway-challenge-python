from typing import Tuple
from uuid import UUID, uuid4

import requests

from payment_gateway_api.enums.payment_status import PaymentStatus
from payment_gateway_api.exception.bank_gateway_exception import BankGatewayException
from payment_gateway_api.exception.event_processiing_exception import EventProcessingException
from payment_gateway_api.model.payment_details import PaymentDetails
from payment_gateway_api.model.post_payment_request import PostPaymentRequest
from payment_gateway_api.repository.payments_repository import PaymentsRepository


class PaymentGatewayService:
    BASE_PATH = "http://localhost:8080"
    PAYMENT_ENDPOINT = "/payments"

    def __init__(self, payments_repository: PaymentsRepository):
        self.payments_repository = payments_repository

    def get_payment_by_id(self, id: UUID) -> PaymentDetails:
        payment = self.payments_repository.get(id)
        if not payment:
            raise EventProcessingException(f"Invalid ID")
        return payment

    def process_payment(self, payment_request: PostPaymentRequest) -> PaymentDetails:
        authorized, authorization_code = self._send_payment_to_bank_gateway(payment_request)
        payment_details = PaymentDetails(
            id=uuid4(),
            authorization_code=authorization_code if authorized else None,
            status=PaymentStatus.AUTHORIZED if authorized else PaymentStatus.REJECTED,
            cardNumberLastFour=int(payment_request.cardNumber[-4:]),
            expiryMonth=payment_request.expiryMonth,
            expiryYear=payment_request.expiryYear,
            currency=payment_request.currency,
            amount=payment_request.amount
        )
        self.payments_repository.add(payment_details)
        return payment_details

    def _send_payment_to_bank_gateway(self, payment_request: PostPaymentRequest) -> Tuple[bool, UUID]:
        response = requests.post(
            url=(self.BASE_PATH + self.PAYMENT_ENDPOINT),
            json={
                "card_number": payment_request.cardNumber,
                "expiry_date": payment_request.expiryDate,
                "currency": payment_request.currency.value,
                "amount": payment_request.amount,
                "cvv": payment_request.cvv
            },
            headers={"Content-Type": "application/json"},
        )
        return self._get_validated_response_from_bank_gateway(response)

    def _get_validated_response_from_bank_gateway(self, response: requests.Response) -> Tuple[bool, UUID]:
        if not response.ok:
            raise BankGatewayException(f"Error from bank gateway: {response.status_code} - {response.text}")

        try:
            data = response.json()
            authorized = data["authorized"]
            authorization_code = data["authorization_code"]
        except Exception:
            raise BankGatewayException(f"Malformed response from bank gateway: {response.text}")

        return (authorized, authorization_code)
