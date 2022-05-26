import re
from Core import *

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def verify_mail_syntax(mail_id):
    if not re.search(regex, mail_id):
        raise HTTPException(status_code=500, detail="Invalid MailID")


async def login_validation(mail_id):
    verify_mail_syntax(mail_id)
    return await login_core(mail_id)

async def register_validation(registration_data):
    verify_mail_syntax(registration_data.mail_id)
    if registration_data.user_type == "client":
        return await registration_client_core(registration_data)
    elif registration_data.user_type == "freelancer":
        return await registration_freelancer_core(registration_data)
    else:
        raise HTTPException(status_code=500, detail="Invalid User Type")

async def get_client_by_mail_id_validation(mail_id):
    verify_mail_syntax(mail_id)
    return await get_client_by_mail_id_core(mail_id)


async def get_freelancer_by_mail_id_validation(mail_id):
    verify_mail_syntax(mail_id)
    return await get_freelancer_by_mail_id_core(mail_id)

async def post_work_validation(work_data):
    if work_data.title != "":
        raise HTTPException(status_code=500, detail="Invalid Title")
    return await post_work_core(work_data)


async def get_active_work_validation():
    return get_active_work_core()


async def get_ongoing_work_validation(freelancer_id):
    return get_ongoing_work_core(freelancer_id)

async def get_finish_work_validation(freelancer_id):
    return get_finish_work_core(freelancer_id)

async def create_proposal_validation(proposal_data):
    return create_proposal_core(proposal_data)