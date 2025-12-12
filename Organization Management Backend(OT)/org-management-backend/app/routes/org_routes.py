from fastapi import APIRouter
from app.models.organization import OrgCreate, OrgUpdate
from app.services.org_service import OrganizationService

router = APIRouter(prefix="/org")

@router.post("/create")
def create_org(data: OrgCreate):
    return OrganizationService.create_org(data)

@router.get("/get")
def get_org(organization_name: str):
    return OrganizationService.get_org(organization_name)

@router.put("/update")
def update_org(data: OrgUpdate):
    return OrganizationService.update_org(data)

@router.delete("/delete")
def delete_org(organization_name: str, admin_email: str):
    return OrganizationService.delete_org(organization_name, admin_email)
