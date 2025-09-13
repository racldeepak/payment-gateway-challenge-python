import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse

from payment_gateway_api.exception.bank_gateway_exception import BankGatewayException
from payment_gateway_api.model.error_response import ErrorResponse


def bank_gateway_exception_handler(request: Request, exc: BankGatewayException):
    logging.error(f"Exception happened: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(message="Error processing payment").dict(),
    )
