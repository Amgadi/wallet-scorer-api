from fastapi import FastAPI
from score_wallet import get_wallet_data

app = FastAPI()


@app.get("/wallet/stats")
async def root(wallet_id: str):
    return get_wallet_data(wallet_id)