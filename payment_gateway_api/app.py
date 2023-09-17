from typing import Dict
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def ping() -> Dict[str, str]:
    return {"app": "payment-gateway-api"}
