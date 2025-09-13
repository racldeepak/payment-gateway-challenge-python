from typing import Dict
from uuid import UUID

from fastapi import APIRouter

from payment_gateway_api.exception.invalid_payment_exception import InvalidPaymentException
from payment_gateway_api.model.post_payment_request import PostPaymentRequest
from payment_gateway_api.model.post_payment_response import PostPaymentResponse
from payment_gateway_api.repository.payments_repository import PaymentsRepository
from payment_gateway_api.service.payment_gateway_service import PaymentGatewayService


router = APIRouter(tags=["payment"])
paymentGatewayService = PaymentGatewayService(PaymentsRepository())


@router.post("/payment", response_model=PostPaymentResponse)
async def process_payment(payment: Dict) -> PostPaymentResponse:
    try:
        payment = PostPaymentRequest(**payment)
    except Exception as e:
        raise InvalidPaymentException(f"Invalid payment request: {str(e)}")
    return paymentGatewayService.process_payment(payment)


# TODO: Change response model to GetPaymentResponse
@router.get("/payment/{id}", response_model=PostPaymentResponse)
async def get_post_payment_event_by_id(id: UUID) -> PostPaymentResponse:
    return paymentGatewayService.get_payment_by_id(id)
