from fastapi import FastAPI
from pydantic import BaseModel

from Validation import *

app = FastAPI()


# Default Validation Modal's
class Registration(BaseModel):
    username: str
    mail_id: str
    password: str
    mobile: str
    user_type: str
    account_creation_type: str


@app.get("/")
async def default():
    return {"message": "Hello there!"}


@app.get("/login/{mail_id}")
async def login(mail_id: str):
    return await login_validation(mail_id)


@app.post("/register")
async def register(registration_data: Registration):
    return await register_validation(registration_data)

@app.get("/get_client_by_mail_id/{mail_id}")
async def get_client_by_mail_id(mail_id: str):
    return await get_client_by_mail_id_validation(mail_id)

@app.get("/get_freelancer_by_mail_id/{mail_id}")
async def get_freelancer_by_mail_id(mail_id: str):
    return await get_freelancer_by_mail_id_validation(mail_id)
