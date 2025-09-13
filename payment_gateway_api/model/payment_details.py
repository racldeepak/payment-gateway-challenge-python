from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from payment_gateway_api.enums.payment_status import PaymentStatus


class PaymentDetails(BaseModel):
    id: UUID
    authorization_code: Optional[str] = None
    status: PaymentStatus
    cardNumberLastFour: int
    expiryMonth: int
    expiryYear: int
    currency: str
    amount: int
