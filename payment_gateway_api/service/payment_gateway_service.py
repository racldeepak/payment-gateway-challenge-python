import logging
from uuid import UUID, uuid4

from payment_gateway_api.enums.payment_status import PaymentStatus
from payment_gateway_api.exception.event_processiing_exception import EventProcessingException
from payment_gateway_api.model.post_payment_request import PostPaymentRequest
from payment_gateway_api.model.post_payment_response import PostPaymentResponse
from payment_gateway_api.repository.payments_repository import PaymentsRepository


class PaymentGatewayService:
    
    def __init__(self, payments_repository: PaymentsRepository):
        self.payments_repository = payments_repository
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_payment_by_id(self, id: UUID) -> PostPaymentResponse:
        self.logger.debug(f"Requesting access to to payment with ID {id}")
        
        payment = self.payments_repository.get(id)
        if not payment:
            raise EventProcessingException(f"Invalid ID")
        return payment

    def process_payment(self, payment_request: PostPaymentRequest) -> PostPaymentResponse:
        # TODO: Integrate with bank gateway
        payment_id = uuid4()
        payment_response = PostPaymentResponse(
            id=payment_id,
            status=PaymentStatus.AUTHORIZED,
            cardNumberLastFour=int(payment_request.cardNumber[-4:]),
            expiryMonth=payment_request.expiryMonth,
            expiryYear=payment_request.expiryYear,
            currency=payment_request.currency,
            amount=payment_request.amount
        )
        self.payments_repository.add(payment_response)
        return payment_response
