from typing import Dict, Union
from uuid import UUID

from payment_gateway_api.model.payment_details import PaymentDetails


class PaymentsRepository:
    payments: Dict[UUID, PaymentDetails] = {}

    def add(self, payment: PaymentDetails) -> None:
        self.payments[payment.id] = payment

    def get(self, id: UUID) -> Union[PaymentDetails, None]:
        return self.payments.get(id)
