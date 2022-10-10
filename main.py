from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from score_wallet import get_wallet_data

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/wallet/stats")
async def root(wallet_id: str):
    return get_wallet_data(wallet_id)