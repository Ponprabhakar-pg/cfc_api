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


@app.post("/post_work")
async def post_work(work_data: Work):
    return await post_work_validation(work_data)


@app.get("/get_active_work")
async def get_active_work():
    return await get_active_work_validation()


@app.get("/get_ongoing_work/{freelancer_id}")
async def get_ongoing_work(freelancer_id: str):
    return await get_ongoing_work_validation(freelancer_id)


@app.get("/get_finished_work/{freelancer_id}")
async def get_finished_work(freelancer_id: str):
    return await get_finish_work_validation(freelancer_id)


@app.post("/create_proposal")
async def create_proposal(proposal_data: Proposal):
    return await create_proposal_validation(proposal_data)


@app.put("/stop_accepting_work_proposal/{work_id}")
async def stop_accepting_work_proposal(work_id):
    return await stop_accepting_work_proposal_validation(work_id)


@app.put("/selected_proposal_for_work/{proposal_id}")
async def selected_proposal_for_work(proposal_id):
    return await selected_proposal_for_work_validation(proposal_id)


@app.put("/update_client_profile/{client_id}/{username}/{mobile}/{address}/{dob}/{description}/{expected_skills}")
async def update_client_profile(client_id, username, mobile, address, dob, description, expected_skills):
    return await update_client_profile_validation(client_id, username, mobile, address, dob, description,
                                                  expected_skills)


@app.put(
    "/update_freelancer_profile/{client_id}/{username}/{mobile}/{address}/{dob}/{description}/{skills}/{linked_in}")
async def update_freelancer_profile(freelancer_id, username, mobile, address, dob, description, skills, linked_in):
    return await update_freelancer_profile_validation(freelancer_id, username, mobile, address, dob, description,
                                                      skills, linked_in)


@app.put("/freelancer_finish_work/{proposal_id}/{feedback_comment}/{feedback_rating}")
async def freelancer_finish_work(proposal_id, feedback_comment, feedback_rating):
    return await freelancer_finish_work_validation(proposal_id, feedback_comment, feedback_rating)


@app.put("/client_finish_work/{proposal_id}/{feedback_comment}/{feedback_rating}")
async def client_finish_work(proposal_id, feedback_comment, feedback_rating):
    return await client_finish_work_validation(proposal_id, feedback_comment, feedback_rating)


@app.get("/verify_mail/{mail_id}")
async def verify_mail(mail_id):
    return await verify_mail_validation(mail_id)


@app.get("/mail_verified/{mail_id}")
async def mail_verified(mail_id):
    return await mail_verified_validation(mail_id)
