import logging
from logging.config import dictConfig as configure_logging
from typing import Dict

from fastapi import FastAPI

from payment_gateway_api.controller.payment_gateway_controller import router as payments_router
from payment_gateway_api.configuration.logger_config import LOGGING_CONFIG
from payment_gateway_api.exception.common_exception_handler import common_exception_handler
from payment_gateway_api.exception.event_processiing_exception import EventProcessingException


configure_logging(LOGGING_CONFIG)

app = FastAPI()
app.include_router(payments_router)

app.add_exception_handler(EventProcessingException, common_exception_handler)


@app.get("/")
async def ping() -> Dict[str, str]:
    logging.info("Ping request received")
    return {"app": "payment-gateway-api"}
