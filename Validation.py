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
    return await get_active_work_core()


async def get_ongoing_work_validation(freelancer_id):
    return await get_ongoing_work_core(freelancer_id)


async def get_finish_work_validation(freelancer_id):
    return await get_finish_work_core(freelancer_id)


async def create_proposal_validation(proposal_data):
    return await create_proposal_core(proposal_data)


async def stop_accepting_work_proposal_validation(work_id):
    return await stop_accepting_work_proposal_core(work_id)


async def selected_proposal_for_work_validation(proposal_id):
    return await selected_proposal_for_work_core(proposal_id)


async def update_client_profile_validation(client_id, username, mobile, address, dob, description, expected_skills):
    return await update_client_profile_core(client_id, username, mobile, address, dob, description, expected_skills)


async def update_freelancer_profile_validation(freelancer_id, username, mobile, address, dob, description, skills,
                                               linked_in):
    return await update_freelancer_profile_core(freelancer_id, username, mobile, address, dob, description, skills,
                                                linked_in)


async def freelancer_finish_work_validation(proposal_id, feedback_comment, feedback_rating):
    return await freelancer_finish_work_core(proposal_id, feedback_rating, feedback_comment)


async def client_finish_work_validation(proposal_id, feedback_comment, feedback_rating):
    return await client_finish_work_core(proposal_id, feedback_rating, feedback_comment)


async def verify_mail_validation(mail_id):
    return await verify_mail_core(mail_id)


async def mail_verified_validation(mail_id):
    return await mail_verified_core(mail_id)