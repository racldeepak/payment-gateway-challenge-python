from datetime import date

from pydantic import BaseModel, root_validator, validator

from payment_gateway_api.enums.currency import Currency


class PostPaymentRequest(BaseModel):
    cardNumber: str
    expiryMonth: int
    expiryYear: int
    currency: Currency
    amount: int
    cvv: int

    @validator('cardNumber')
    def validate_cardNumber(cls, value):
        if (len(value) < 14 or len(value) > 19) or (not value.isdigit()):
            raise ValueError('Card number must be a numeric string between 14 and 19 digits long')
        return value

    @validator('expiryMonth')
    def validate_expiryMonth(cls, value):
        if (value < 1 or value > 12):
            raise ValueError('Expiry month must be between 1 and 12')
        return value

    @validator('expiryYear')
    def validate_expiryYear(cls, value):
        current_year = date.today().year
        if (value < current_year or value > current_year + 6):
            raise ValueError(f'Invalid expiry year')
        return value
    
    @validator('cvv')
    def validate_cvv(cls, value):
        if (value < 100 or value > 9999):
            raise ValueError('CVV must be a 3 or 4-digit number')
        return value
    
    @validator('amount')
    def validate_amount(cls, value):
        if value is not None and value <= 0:
            raise ValueError('Invalid amount')
        return value

    @root_validator
    def validate_expiry_date(cls, values):
        today = date.today()
        expiry_month = values.get('expiryMonth')
        expiry_year = values.get('expiryYear')
        
        if expiry_month and expiry_year:
            expiry_date = date(year=expiry_year, month=expiry_month, day=today.day)
            if expiry_date < today:
                raise ValueError('Expiry date cannot be in the past')
        return values

    @property
    def expiry_date(self) -> str:
        return f"{self.expiryMonth:02}/{self.expiryYear}"
