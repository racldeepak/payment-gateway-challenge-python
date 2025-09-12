from pydantic import BaseModel


class PostPaymentRequest(BaseModel):
    cardNumberLastFour: int
    expiryMonth: int
    expiryYear: int
    currency: str
    amount: int
    cvv: int
    
    @property
    def expiry_date(self) -> str:
        return f"{self.expiryMonth:02}/{self.expiryYear}"
