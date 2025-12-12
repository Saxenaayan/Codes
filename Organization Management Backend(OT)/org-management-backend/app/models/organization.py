from pydantic import BaseModel

class OrgCreate(BaseModel):
    organization_name: str
    email: str
    password: str

class OrgGet(BaseModel):
    organization_name: str

class OrgUpdate(BaseModel):
    organization_name: str
    email: str
    password: str
