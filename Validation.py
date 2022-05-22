import re
from Core import *

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


async def login_validation(mail_id):
    if not re.search(regex, mail_id):
        raise HTTPException(status_code=500, detail="Invalid MailID")
    return await login_core(mail_id)

async def register_validation(registration_data):
    if not re.search(regex, registration_data.mail_id):
        raise HTTPException(status_code=500, detail="Invalid MailID")
    if registration_data.user_type == "client":
        return await registration_client_core(registration_data)
    elif registration_data.user_type == "freelancer":
        return await registration_freelancer_core(registration_data)
    else:
        raise HTTPException(status_code=500, detail="Invalid User Type")

async def get_client_by_mail_id_validation(mail_id):
    if not re.search(regex, mail_id):
        raise HTTPException(status_code=500, detail="Invalid MailID")
    return await get_client_by_mail_id_core(mail_id)


async def get_freelancer_by_mail_id_validation(mail_id):
    if not re.search(regex, mail_id):
        raise HTTPException(status_code=500, detail="Invalid MailID")
    return await get_freelancer_by_mail_id_core(mail_id)