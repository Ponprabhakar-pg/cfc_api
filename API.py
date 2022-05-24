from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Utils.ModalClasses import *
from Validation import *

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
