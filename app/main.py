from typing import Union

from fastapi import FastAPI, HTTPException
from app.cognito_service import CognitoAuthService
from pydantic import BaseModel

app = FastAPI()
cognito_service = CognitoAuthService()

class SignUpRequest(BaseModel):
    client_id: str
    username: str
    password: str
    email: str
    phone_number: str

class AuthInitiateRequest(BaseModel):
    client_id: str
    username: str

class VerifyLoginRequest(BaseModel):
    client_id: str
    code: str
    username: str
    session: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



@app.post("/signup")
def signup(request: SignUpRequest):
    try:
        response = cognito_service.sign_up(
            request.client_id,
            request.username, 
            request.password, 
            request.email, 
            request.phone_number
        )
        return {"message": "User signed up successfully", "response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/initiate")
def initiate_auth(request: AuthInitiateRequest):
    try:
        response = cognito_service.initiate_auth(request.client_id,request.username)
        return {"message": "Authentication initiated", "session": response.get('Session')}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/auth/verify")
def verify_login(request: VerifyLoginRequest):
    try:
        auth_result = cognito_service.verify_login(
            request.client_id,
            request.code, 
            request.username, 
            request.session
        )
        return {"message": "Login successful", "auth_result": auth_result}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))