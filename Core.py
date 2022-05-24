import pymongo
from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime

from DbConfig import *
from Utils.HelperDictionaries import *

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
    if client is None:
        raise HTTPException(status_code=500, detail="No Client Exist")
    return client


async def get_freelancer_by_mail_id_core(mail_id):
    my_col = my_db[FreelancerCollection]
    freelancer = my_col.find_one({"mail_id": mail_id})
    if freelancer is None:
        raise HTTPException(status_code=500, detail="No Freelancer Exist")
    return freelancer
