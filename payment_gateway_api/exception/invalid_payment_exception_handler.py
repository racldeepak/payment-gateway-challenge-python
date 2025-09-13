import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse

from payment_gateway_api.exception.invalid_payment_exception import InvalidPaymentException
from payment_gateway_api.model.error_response import ErrorResponse


def invalid_payment_exception_handler(request: Request, exc: InvalidPaymentException):
    logging.error(f"Exception happened: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(message="Rejected: Invalid payment request").dict(),
    )
