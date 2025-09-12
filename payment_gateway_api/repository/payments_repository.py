from typing import Dict, Union
from uuid import UUID

from payment_gateway_api.model.post_payment_response import PostPaymentResponse


class PaymentsRepository:
    payments: Dict[UUID, PostPaymentResponse] = {}

    def add(self, payment: PostPaymentResponse) -> None:
        self.payments[payment.id] = payment

    def get(self, id: UUID) -> Union[PostPaymentResponse, None]:
        return self.payments.get(id)
