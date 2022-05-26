from pydantic import BaseModel


# Default Validation Modal's
class Registration(BaseModel):
    username: str
    mail_id: str
    password: str
    mobile: str
    user_type: str
    account_creation_type: str

class Work(BaseModel):
    title: str
    short_description: str
    long_description: str
    amount: str
    duration: str
    documents: str
    skills_required: list
    client_id: str
    # work_status: int
    # accepted_proposal_id: str
    # ongoing_proposal_id: list

class Proposal(BaseModel):
    work_id: str
    client_id: str
    freelancer_id: str
    bid_amount: str
    bid_duration: str
    bid_description: str
