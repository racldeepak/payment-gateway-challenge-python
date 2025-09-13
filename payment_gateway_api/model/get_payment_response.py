from uuid import UUID
from pydantic import BaseModel

from payment_gateway_api.enums.currency import Currency
from payment_gateway_api.enums.payment_status import PaymentStatus


class GetPaymentResponse(BaseModel):
    id: UUID
    status: PaymentStatus
    cardNumberLastFour: int
    expiryMonth: int
    expiryYear: int
    currency: Currency
    amount: int
