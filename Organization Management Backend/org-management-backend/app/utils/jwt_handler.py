import jwt
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM

def create_jwt(admin_id, org_name):
    payload = {
        "admin_id": str(admin_id),
        "org_name": org_name,
        "exp": datetime.utcnow() + timedelta(hours=5)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
