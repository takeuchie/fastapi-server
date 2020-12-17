from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

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

# In memory database 
db = [{
    'username': 'admin@test.com',
    'email': 'admin@test.com',
    'hashed_password': 'hashedPassw0rd!',
}] 

# Sample model
class User(BaseModel):
    username: str
    email: Optional[str] = None
    state: Optional[str] = None
    file_status: Optional[str] = None

class UserInDB(User):
    hashed_password: str

# Endpoints / Routes
@app.get('/')
def index():
    return 'Backend API Works'

@app.get('/users')
def get_users():
    return db
