from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

# Instantiate app object
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In memory database 
db = [{
    'username': 'admin@test.com',
    'email': 'admin@test.com',
    'hashed_password': 'hashedPassw0rd!',
}] 

class User(BaseModel):
    username: str
    email: Optional[str] = None
    state: Optional[str] = None
    file_status: Optional[str] = None

class UserInDB(User):
    hashed_password: str

def get_user(users, username: str):
    for x in users:
        if x['email'] == username:
            return UserInDB(**x)
    return None

def hash_password(password: str):
    return "hashed" + password

def decode_token(token):
    # This doesn't provide any security at all
    user = get_user(db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.get('/')
def index():
    return 'Backend API Works'

@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    user = get_user(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    hashed_pass = hash_password(form_data.password)
    if not hashed_pass == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get('/users')
def get_users():
    return db

@app.get('/users/{user_id}')
def get_user_by_id(user_id: int):
    if user_id < 0 and user_id > len(db):
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    return db[user_id-1]

@app.post('/users')
def create_user(user: User):
    db.append(user.dict())
    return db[-1]

# @app.put('/users/{user_id}')
# def update_user(user_id: int, user: User):

@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db.pop(user_id-1)
    return 'User deleted'

@app.get("/users/me")
async def get_users_me(current_user: User = Depends(get_current_user)):
    return current_user