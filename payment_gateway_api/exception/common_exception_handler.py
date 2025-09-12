import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse

from payment_gateway_api.exception.event_processiing_exception import EventProcessingException
from payment_gateway_api.model.error_response import ErrorResponse


def common_exception_handler(request: Request, exc: EventProcessingException):
    logging.error(f"Exception happened: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(message="Page not found").dict(),
    )
