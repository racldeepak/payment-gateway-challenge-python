import logging
from uuid import UUID

from fastapi import APIRouter

from payment_gateway_api.model.post_payment_response import PostPaymentResponse
from payment_gateway_api.repository.payments_repository import PaymentsRepository
from payment_gateway_api.service.payment_gateway_service import PaymentGatewayService


router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)


paymentGatewayService = PaymentGatewayService(PaymentsRepository())


@router.get("/{id}", response_model=PostPaymentResponse)
async def get_post_payment_event_by_id(id: UUID) -> PostPaymentResponse:
    logging.info(f"Get payment request received for payment ID: {id}")
    return paymentGatewayService.get_payment_by_id(id)
