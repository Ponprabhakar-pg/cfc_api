from pydantic import BaseModel


# Default Validation Modal's
class Registration(BaseModel):
    username: str
    mail_id: str
    password: str
    mobile: str
    user_type: str
    account_creation_type: str
