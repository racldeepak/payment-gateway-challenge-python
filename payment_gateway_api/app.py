import logging
from logging.config import dictConfig as configure_logging
from typing import Dict

from fastapi import FastAPI

from payment_gateway_api.configuration.logger_config import LOGGING_CONFIG
from payment_gateway_api.controller.payment_gateway_controller import router as payments_router
from payment_gateway_api.exception.invalid_payment_exception_handler import invalid_payment_exception_handler
from payment_gateway_api.exception.bank_gateway_exception import BankGatewayException
from payment_gateway_api.exception.bank_gateway_exception_handler import bank_gateway_exception_handler
from payment_gateway_api.exception.event_processing_exception_handler import event_processing_exception_handler
from payment_gateway_api.exception.event_processiing_exception import EventProcessingException
from payment_gateway_api.exception.invalid_payment_exception import InvalidPaymentException


configure_logging(LOGGING_CONFIG)

app = FastAPI()
app.include_router(payments_router)

app.add_exception_handler(EventProcessingException, event_processing_exception_handler)
app.add_exception_handler(BankGatewayException, bank_gateway_exception_handler)
app.add_exception_handler(InvalidPaymentException, invalid_payment_exception_handler)


# TODO: Log access requests


@app.get("/")
async def ping() -> Dict[str, str]:
    logging.info("Ping request received")
    return {"app": "payment-gateway-api"}
