# `/login` endpoint is responsible for authenticating the user and generating the JWT access token. The `admin_only` dependency checks whether the current user has admin privileges, restricting access to certain endpoints accordingly. The `get_current_user` dependency validates the provided token and retrieves the user information for authorization purposes.
                                                                                                                                                                                                                                                                                                                                          
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample data storage
data = []

# Define request body models
class Item(BaseModel):
    name: str
    price: float

class User(BaseModel):
    username: str
    password: str
    is_admin: bool

# Hash and verify password
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Authenticate user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# Encode JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

# Mock user database
users_db = [
    {
        "username": "admin",
        "password": get_password_hash("admin123"),
        "is_admin": True
    },
    {
        "username": "user",
        "password": get_password_hash("user123"),
        "is_admin": False
    }
]

# Get user by username
def get_user(username):
    for user in users_db:
        if user["username"] == username:
            return User(**user)
    return None

# Authenticate and generate access token
async def login(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}

# Dependency function to validate and retrieve token credentials
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token_data = verify_token(credentials.credentials)
    return get_user(token_data.username)

# Authorization check for admin-only endpoints
async def admin_only(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")

# GET request to retrieve all items
@app.get("/items")
async def get_items():
    return data

# POST request to add a new item
@app.post("/items")
async def add_item(item: Item, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        data.append(item)
        return {"message": "Item added successfully"}
    raise HTTPExcepätion(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")

# PUT request to update an existing item
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        if item_id < len(data):
            data[item_id] = item
            return {"message": "Item updated successfully"}
        raise HTTPExcepion(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    raise HTTPExcepion(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")

# DELETE request to remove an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        if item_id < len(data):
            del data[item_id]
            return {"message": "Item deleted successfully"}
        raise HTTPExcepion(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    raise HTTPExcepion(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")

# Login endpoint to generate access token
@app.post("/login")
async def login_route(username: str, password: str):
    return await login(username, password)
