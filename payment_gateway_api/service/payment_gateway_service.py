import logging
from uuid import UUID, uuid4

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

    def process_payment(self, payment_request: PostPaymentRequest) -> UUID:
        return uuid4()
