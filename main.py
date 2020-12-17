from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field

# Instantiate app object
app = FastAPI()

# Handle cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Security(BaseModel):
    fair_market_value: float
    quantity: int

# Endpoints / Routes
@app.get('/')
def index():
    return 'Backend API Works'

@app.post('/securities')
def estimate(security: Security):
    if not security.fair_market_value > 0:
        raise HTTPException(status_code=400, detail="Invalid value given")

    if not security.quantity > 0:
        raise HTTPException(status_code=400, detail="Invalid value given")

    return security.fair_market_value * security.quantity