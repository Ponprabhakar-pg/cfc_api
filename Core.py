import pymongo
from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime
from random import randint

from Utils.DBConfig import *
from Utils.HelperDictionaries import *
from Utils.Mailer import mail_trigger

my_client = pymongo.MongoClient(MongoDBConnectionString)
my_db = my_client[DBName]


async def login_core(mail_id):
    my_col = my_db[UserCollection]
    user_data = my_col.find_one({"mail_id": mail_id})
    if user_data is None:
        raise HTTPException(status_code=500, detail="No User Exist")
    return user_data


async def registration_client_core(registration_data):
    my_col1 = my_db[ClientCollection]
    my_col2 = my_db[UserCollection]

    client = client_dict.copy()
    overall_user = user_dict.copy()

    client['created_at'] = str(datetime.now())
    client['username'] = registration_data.username
    client['password'] = registration_data.password
    client['mobile'] = registration_data.mobile
    client['mail_id'] = registration_data.mail_id
    client['account_creation_type'] = registration_data.account_creation_type
    client['_id'] = str(uuid4())

    overall_user['_id'] = str(uuid4())
    overall_user['created_at'] = str(datetime.now())
    overall_user['username'] = registration_data.username
    overall_user['password'] = registration_data.password
    overall_user['mail_id'] = registration_data.mail_id
    overall_user['user_type'] = "client"
    overall_user['account_creation_type'] = registration_data.account_creation_type
    overall_user['mobile'] = registration_data.mobile
    if my_col2.find_one({"mail_id": registration_data.mail_id}) is not None:
        raise HTTPException(status_code=500, detail="User Already Exist")
    my_col1.insert_one(client)
    my_col2.insert_one(overall_user)

    return {"message": "Client Created Successfully"}


async def registration_freelancer_core(registration_data):
    my_col1 = my_db[FreelancerCollection]
    my_col2 = my_db[UserCollection]

    freelancer = freelancer_dict.copy()
    overall_user = user_dict.copy()

    freelancer['_id'] = str(uuid4())
    freelancer['created_at'] = str(datetime.now())
    freelancer['username'] = registration_data.username
    freelancer['password'] = registration_data.password
    freelancer['mobile'] = registration_data.mobile
    freelancer['mail_id'] = registration_data.mail_id
    freelancer['account_creation_type'] = registration_data.account_creation_type

    overall_user['_id'] = str(uuid4())
    overall_user['created_at'] = str(datetime.now())
    overall_user['username'] = registration_data.username
    overall_user['password'] = registration_data.password
    overall_user['mail_id'] = registration_data.mail_id
    overall_user['user_type'] = "freelancer"
    overall_user['account_creation_type'] = registration_data.account_creation_type
    overall_user['mobile'] = registration_data.mobile
    if my_col2.find_one({"mail_id": registration_data.mail_id}) is not None:
        raise HTTPException(status_code=500, detail="User Already Exist")

    my_col1.insert_one(freelancer)
    my_col2.insert_one(overall_user)

    return {"message": "Freelancer Created Successfully"}


async def get_client_by_mail_id_core(mail_id):
    my_col = my_db[ClientCollection]
    client = my_col.find_one({"mail_id": mail_id})
    client['password'] = "******"
    if client is None:
        raise HTTPException(status_code=500, detail="No Client Exist")
    return client


async def get_freelancer_by_mail_id_core(mail_id):
    my_col = my_db[FreelancerCollection]
    freelancer = my_col.find_one({"mail_id": mail_id})
    freelancer['password'] = "******"
    if freelancer is None:
        raise HTTPException(status_code=500, detail="No Freelancer Exist")
    return freelancer


async def post_work_core(work_data):
    my_col = my_db[WorkCollection]
    client_col = my_db[ClientCollection]
    work = work_dict.copy()
    work['_id'] = str(uuid4())
    work['created_at'] = str(datetime.now())
    work['title'] = work_data.title
    work['short_description'] = work_data.short_description
    work['long_description'] = work_data.long_description
    work['amount'] = work_data.amount
    work['duration'] = work_data.duration
    work['client_id'] = work_data.client_id
    work['documents'] = work_data.documents
    work['skills_required'] = work_data.skills_required

    client_col.update_one({"_id": work['client_id']}, {'$push': {'posted_work': work['_id']}})
    my_col.insert_one(work)
    return {"message": "Work Created Successfully"}


async def get_active_work_core():
    work_col = my_db[WorkCollection]
    work_array = work_col.find({"work_status": 0})
    result = []
    for work in work_array:
        result.append(work)
    return result


async def get_ongoing_work_core(freelancer_id):
    work_col = my_db[WorkCollection]
    freelancer_col = my_db[FreelancerCollection]
    client_col = my_db[ClientCollection]
    freelancer_data = freelancer_col.find_one({'_id': freelancer_id})
    if (freelancer_data['ongoing_work']) > 0:
        ongoing_work = []
        for work_id in freelancer_data['ongoing_work']:
            work = work_col.find_one({'_id': work_id})
            work['client_details'] = client_col.find_one({'_id': work['client_id']})
            ongoing_work.append(work)
        return ongoing_work
    return []


async def get_finish_work_core(freelancer_id):
    work_col = my_db[WorkCollection]
    freelancer_col = my_db[FreelancerCollection]
    client_col = my_db[ClientCollection]
    freelancer_data = freelancer_col.find_one({'_id': freelancer_id})
    if (freelancer_data['finished_work']) > 0:
        finished_work = []
        for work_id in freelancer_data['finished_work']:
            work = work_col.find_one({'_id': work_id})
            work['client_details'] = client_col.find_one({'_id': work['client_id']})
            finished_work.append(work)
        return finished_work
    return []


async def create_proposal_core(proposal_data):
    proposal_col = my_db[ProposalCollection]
    work_col = my_db[WorkCollection]
    freelancer_col = my_db[FreelancerCollection]
    proposal = proposal_dict.copy()
    proposal['_id'] = str(uuid4())
    proposal['created_at'] = str(datetime.now())
    proposal['work_id'] = proposal_data.work_id
    proposal['client_id'] = proposal_data.client_id
    proposal['freelancer_id'] = proposal_data.freelancer_id
    proposal['bid_amount'] = proposal_data.bid_amount
    proposal['bid_duration'] = proposal_data.bid_duration
    proposal['bid_description'] = proposal_data.bid_description
    proposal_col.insert_one(proposal)
    work_col.update_one({"_id": proposal['work_id']}, {'$push': {'proposals': proposal['_id']}})
    result = freelancer_col.update_one({'_id': proposal['freelancer_id']}, {'$push': {'applied_proposal': proposal['_id']}})
    if result.modified_count > 0:
        return {"message": "Proposal Created Successfully"}
    else:
        return {"message": "Unable to create proposal"}


async def stop_accepting_work_proposal_core(work_id):
    work_col = my_db[WorkCollection]
    result = work_col.update_one({'_id': work_id}, {'$set': {'work_status': 1}})
    if result.modified_count > 0:
        return True
    else:
        return False

async def selected_proposal_for_work_core(proposal_id):
    proposal_col = my_db[ProposalCollection]
    client_col = my_db[ClientCollection]
    freelancer_col = my_db[FreelancerCollection]
    work_col = my_db[WorkCollection]
    proposal = proposal_col.find_one({'_id': proposal_id})
    if proposal['proposal_status'] == 0:
        proposal_col.update_one({'_id': proposal_id}, {'$set': {'proposal_status': 1}})
        freelancer_col.update_one({'_id': proposal['freelancer_id']}, {'$push': {'ongoing_proposal': proposal_id}})
        work_col.update_one({'_id': proposal['work_id']}, {'$set': {'accepted_proposal_id': proposal['_id']}})
        work_col.update_one({'_id': proposal['work_id']}, {'$set': {'work_status': 2}})
        result = client_col.update_one({'_id': proposal['client_id']}, {'$push': {'ongoing_work': proposal['work_id']}})
        if result.modified_count > 0:
            return True
        else:
            return False
    return False

async def update_client_profile_core(client_id, username, mobile, address, dob, description, expected_skills):
    client_col = my_db[ClientCollection]
    result = client_col.update_one({'_id': client_id}, {'$set': {'username': username, 'mobile': mobile, 'address': address, 'dob': dob, 'description': description, 'expected_skills': expected_skills, 'profile_status': 1}})
    client = client_col.find_one({'mail_id': client_id})
    if client['mail_verification_status'] == 1:
        client_col.update_one({'mail_id': client_id}, {'$set': {'account_status': 1}})
    if result.modified_count > 0:
        return True
    else:
        return False

async def update_freelancer_profile_core(freelancer_id, username, mobile, address, dob, description, skills, linked_in):
    freelancer_col = my_db[FreelancerCollection]
    result = freelancer_col.update_one({'_id': freelancer_id}, {'$set': {'username': username, 'mobile': mobile, 'address': address, 'dob': dob, 'description': description, 'skills': skills, 'linked_in': linked_in, 'profile_status': 1}})
    freelancer = freelancer_col.find_one({'_id': freelancer_id})
    if freelancer['mail_verification_status'] == 1:
        freelancer_col.update_one({'mail_id': freelancer_id}, {'$set': {'account_status': 1}})
    if result.modified_count > 0:
        return True
    else:
        return False


async def freelancer_finish_work_core(proposal_id, feedback_rating, feedback_comment):
    proposal_col = my_db[ProposalCollection]
    client_col = my_db[ClientCollection]
    freelancer_col = my_db[FreelancerCollection]
    work_col = my_db[WorkCollection]
    proposal = proposal_col.find_one({'_id': proposal_id})
    proposal_col.update_one({'_id': proposal_id}, {'$set': {'proposal_status': 2}})
    feedback = feedback_dict.copy()
    feedback['work_id'] = proposal['work_id']
    feedback['feedback'] = feedback_comment
    feedback['rating'] = feedback_rating
    client_col.update_one({'_id': proposal['client_id']}, {'$push': {'feedbacks': feedback}})
    work = work_col.find_one({'_id': proposal['work_id']})
    if(work['work_status'] == 2):
        work_col.update_one({'_id': proposal['work_id']}, {'$set': {'work_status': 3}})
    else:
        work_col.update_one({'_id': proposal['work_id']}, {'$set': {'work_status': 5}})
    result = freelancer_col.update_one({'_id': proposal['freelancer_id']}, {'$push': {'finished_proposal': proposal_id}})
    if result.modified_count > 0:
        return True
    else:
        return False


async def client_finish_work_core(proposal_id, feedback_rating, feedback_comment):
    proposal_col = my_db[ProposalCollection]
    client_col = my_db[ClientCollection]
    freelancer_col = my_db[FreelancerCollection]
    work_col = my_db[WorkCollection]
    proposal = proposal_col.find_one({'_id': proposal_id})
    proposal_col.update_one({'_id': proposal_id}, {'$set': {'proposal_status': 2}})
    feedback = feedback_dict.copy()
    feedback['work_id'] = proposal['work_id']
    feedback['feedback'] = feedback_comment
    feedback['rating'] = feedback_rating
    freelancer_col.update_one({'_id': proposal['freelancer_id']}, {'$push': {'feedbacks': feedback}})
    work = work_col.find_one({'_id': proposal['work_id']})
    if(work['work_status'] == 2):
        work_col.update_one({'_id': proposal['work_id']}, {'$set': {'work_status': 4}})
    else:
        work_col.update_one({'_id': proposal['work_id']}, {'$set': {'work_status': 5}})
    result = client_col.update_one({'_id': proposal['client_id']}, {'$push': {'finished_work': proposal['work_id']}})
    if result.modified_count > 0:
        return True
    else:
        return False


async def verify_mail_core(mail_id):
    otp = randint(100000, 999999)
    await mail_trigger(mail_id,otp)
    return {"OTP": otp}


async def mail_verified_core(mail_id):
    my_col = my_db[UserCollection]
    user_data = my_col.find_one({'mail_id': mail_id})
    if user_data['user_type'] == 'freelancer':
        freelancer_col = my_db[FreelancerCollection]
        result = freelancer_col.update_one({'mail_id': mail_id}, {'$set': {'mail_verification_status': 1}})
        freelancer = freelancer_col.find_one({'mail_id': mail_id})
        if freelancer['profile_status'] == 1:
            freelancer_col.update_one({'mail_id': mail_id}, {'$set': {'account_status': 1}})
        if result.modified_count > 0:
            return True
        return False
    else:
        client_col = my_db[ClientCollection]
        result = client_col.update_one({'mail_id': mail_id}, {'$set': {'mail_verification_status': 1}})
        client = client_col.find_one({'mail_id': mail_id})
        if client['profile_status'] == 1:
            client_col.update_one({'mail_id': mail_id}, {'$set': {'account_status': 1}})
        if result.modified_count > 0:
            return True
        return False